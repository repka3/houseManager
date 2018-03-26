import socketserver, socket, queue, threading, time, traceback,json, datetime

KILL_COND = False
HOST = socket.gethostname()
PORT_CLIENT_SERVER = 9500

CONSOLE_PRINT=True
def server_msg_(msg):
    if CONSOLE_PRINT:
        print("[{}] {}".format(datetime.datetime.now(),msg))

class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None
    list_queue = []

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance

    def get_queue_byname(self, name):
        name = name.strip()
        for i in range(len(self.list_queue)):
            this_queue = self.list_queue[i]
            if this_queue['Name'] == name:
                return this_queue['q']
        q = queue.Queue()
        self.list_queue.append({'Name': name, 'q': q})
        server_msg_("Cant find queue for {}, creating new one.".format(name))
        return q

    def destroy_queue_byname(self, name):
        for i in range(len(self.list_queue)):
            this_queue = self.list_queue[i]
            if this_queue['Name'] == name:
                server_msg_("found the list for name {}. List was size={}".format(name, len(self.list_queue)))
                del self.list_queue[i]
                server_msg_("now list size is:{}".format(len(self.list_queue)))
                return
                server_msg_("Queue was not present for name:{},leaving as it was".format(name))

    def get_all_queues_name(self):
        l = []
        for i in range(len(self.list_queue)):
            thisq = self.list_queue[i]
            l.append(thisq['Name'])
        return l


class ClientProblem(Exception):
    pass


class SingleTCPHandler(socketserver.BaseRequestHandler):
    """One instance per connection.  Override handle(self) to customize action."""
    pseudo_name = None
    DEBUG_LOCK = False
    DEBUG_SOCKETMSG = True
    L = threading.Lock()
    count = 0
    def handle(self):
        server_msg_("Thread spawned to serves addr:" + str(self.client_address))
        self.count = 0
        try:
            while True:
                jsonmsg = None
                # server_msg_("ml acquiring..")
                #self.acquireLock("ML")
                # server_msg_("ml acquired..")
                #server_msg_("Socket ready. Get data.")
                dictmsg = self.recvDict()
                responseDict = self.handleClientMessageGetDictResponse(dictmsg)
                self.sendDict(responseDict)
                if KILL_COND:
                    raise Exception("KILL_COND: General exit request, closing")

                #self.releaseLock("ML")
        except ClientProblem as e:
            server_msg_("Client problem:" + str(self.client_address) + " disconnect or error. Goodbye world!")
        except Exception as e:
            server_msg_("unhandled exception in SingleTCPRequest e:" + str(e))
            traceback.print_exc()
        finally:
            # self.KILL_MY_SON=True
            if self.pseudo_name:
                SingletonMixin.instance().destroy_queue_byname(str(self.pseudo_name))
            self.request.close()
            server_msg_("\nHandle singleTCPHandler dead.\n")
            #self.releaseLock("ML")

    def handleClientMessageGetDictResponse(self, dictmsg):

        if dictmsg['msgtype'] == "HELLO":
            if self.pseudo_name is not None:
                server_msg_("Duplicate hello msg? oldname:" + self.pseudo_name)
                return self.createNackDict("Duplicate HELLO msg.")
            self.pseudo_name = str(dictmsg['client_name']).strip()
            ##prob a work around, create queue now
            SingletonMixin.instance().get_queue_byname(self.pseudo_name)
            server_msg_("Hello msg recv. Got client name: " + self.pseudo_name)
            return self.createAckDict()

        else:
            msgtype = str(dictmsg['msgtype']).strip()

            # errors checks
            if not msgtype or len(msgtype) < 3:
                return self.createNackDict("Bad msgtype: {}".format(msgtype))
            if self.pseudo_name is None:
                return self.createNackDict("Client should send HELLO first.")
            if str(dictmsg['client_name']).strip() != self.pseudo_name:
                raise Exception("wtf? processing message not mine.:" + str(dictmsg))

            # apparently no errors so lets process msg
            if msgtype == "COMMAND":
                cmd = str(dictmsg['command']).strip()
                if not cmd or len(cmd) < 3:
                    return self.createNackDict("Bad command: {}".format(cmd))
                for_client = str(dictmsg['for_client']).strip()
                if not cmd or len(cmd) < 3:
                    return self.createNackDict("Bad for_client: {}".format(for_client))
                server_msg_("\nWe got a command: {} for client:{}\n".format(cmd, for_client))
                q = SingletonMixin.instance().get_queue_byname(for_client)
                q.put(dictmsg)
                return self.createAckDict()
            if msgtype == "LISTCLIENTS":
                l = SingletonMixin.instance().get_all_queues_name()
                data = {
                    'msgtype': 'SRVRESPONSE_CLIENTS',
                    'clients': l
                }
                return data
            if msgtype == "GETALLMSGFORME":
                q = SingletonMixin.instance().get_queue_byname(self.pseudo_name)
                l = []
                i = True
                while i:
                    if q.empty():
                        break
                    i = q.get()
                    l.append(i)
                data = {
                    'msgtype': 'SRVRESPONSE_MSG',
                    'count': len(l),
                    'msgs': l
                }
                return data

    def sendDict(self, data):
        # self.acquireLock("-sendJson-")
        try:
            if not data or not data['msgtype']:
                raise Exception("Malformed data to send in socket")
            msg = json.dumps(data)
            if not msg:
                raise Exception("Cant convert data to json for send in socket")
            encoded = msg.encode('utf-8');
            self.request.send(encoded)
            if self.DEBUG_SOCKETMSG:
                server_msg_("#SCK Sent:   {}".format(encoded))
        except Exception as e:
            server_msg_("Exception in sendJson: {}".format(e))
            raise e


    def recvDict(self, buffersize=4096):
        # self.acquireLock("-recvJson-")
        try:
            data = self.request.recv(buffersize)
            if data == b'':
                raise ClientProblem("client disconnect?")
            if not data:
                raise ClientProblem("Bad data from client")
            text = data.decode('utf-8')
            if self.DEBUG_SOCKETMSG:
                print(f"#SCK Recv:   {text}")
            if not text or len(text) < 5:
                raise ClientProblem("Bad text decoded from client")
            msg = json.loads(text)
            if not msg or not msg['msgtype']:
                raise ClientProblem("Bad json from client")
            return msg
        except ClientProblem as e:
            raise e
        except Exception as e:
            server_msg_("Unhandled Exception in recvJson: {}".format(e))
            raise e


    def createAckDict(self):
        data = {
            'msgtype': 'ACK'
        }
        return data

    def createNackDict(self, msg):
        dic = {
            'msgtype': 'NACK',
            'reason': msg
        }
        return dic

    def acquireLock(self, msg):
        if self.DEBUG_LOCK:
            server_msg_("Acquiring lock: {}".format(msg))
        self.L.acquire()
        if self.DEBUG_LOCK:
            server_msg_("Got       lock: {}".format(msg))

    def releaseLock(self, msg):
        if self.DEBUG_LOCK:
            server_msg_("Releasing lock: {}".format(msg))
        self.L.release()
        if self.DEBUG_LOCK:
            server_msg_("Free      lock: {}".format(msg))


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":
    server = SimpleServer((HOST, PORT_CLIENT_SERVER), SingleTCPHandler)
    server_msg_("Server created. Starting serve_forever.. HOST:" + str(HOST) + " PORT:" + str(PORT_CLIENT_SERVER))
    try:
        # threading.Thread(target=server.serve_forever,daemon=True).start()
        server.serve_forever()
    except KeyboardInterrupt:
        server_msg_("Main server interrupted.")

    finally:
        server_msg_("Finally closing server.")
        server.shutdown()
        server.server_close()

        GENERAL_EXIT_REQUEST = True
        # os.kill(os.getpid(),signal.SIGTERM) # send myself sigterm
