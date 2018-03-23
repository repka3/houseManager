import socketserver, socket, queue, threading, select, time, traceback
from pprint import pprint
import json

KILL_COND = False
HOST = socket.gethostname()
PORT_CLIENT_SERVER = 9500


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
        print("Cant find queue for {}, creating new one.".format(name))
        return q

    def destroy_queue_byname(self, name):
        for i in range(len(self.list_queue)):
            this_queue = self.list_queue[i]
            if this_queue['Name'] == name:
                print("found the list for name {}. List was size={}".format(name, len(self.list_queue)))
                del self.list_queue[i]
                print("now list size is:{}".format(len(self.list_queue)))
                return
        print("Queue was not present for name:{},leaving as it was".format(name))

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
        print("Thread spawned to serves addr:" + str(self.client_address))
        self.count = 0
        try:
            while True:
                jsonmsg = None
                # print("ml acquiring..")
                #self.acquireLock("ML")
                # print("ml acquired..")
                print("Socket ready. Get data.")
                dictmsg = self.recvDict()
                responseDict = self.handleClientMessageGetDictResponse(dictmsg)
                self.sendDict(responseDict)
                if KILL_COND:
                    raise Exception("KILL_COND: General exit request, closing")

                #self.releaseLock("ML")
        except ClientProblem as e:
            print("Client problem:" + str(self.client_address) + " disconnect or error. Goodbye world!")
        except Exception as e:
            print("unhandled exception in SingleTCPRequest e:" + str(e))
            traceback.print_exc()
        finally:
            # self.KILL_MY_SON=True
            if self.pseudo_name:
                SingletonMixin.instance().destroy_queue_byname(str(self.pseudo_name))
            self.request.close()
            print("\nHandle singleTCPHandler dead.\n")
            #self.releaseLock("ML")

    def handleClientMessageGetDictResponse(self, dictmsg):

        if dictmsg['msgtype'] == "HELLO":
            if self.pseudo_name is not None:
                print("Duplicate hello msg? oldname:" + self.pseudo_name)
                return self.createNackDict("Duplicate HELLO msg.")
            self.pseudo_name = str(dictmsg['client_name']).strip()
            ##prob a work around, create queue now
            SingletonMixin.instance().get_queue_byname(self.pseudo_name)
            print("Hello msg recv. Got client name: " + self.pseudo_name)
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
                print("\nWe got a command: {} for client:{}\n".format(cmd, for_client))
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
                print("#SCK Sent:   {}".format(encoded))
        except Exception as e:
            print("Exception in sendJson: {}".format(e))
            raise e
        finally:
            # self.releaseLock("-sendJson-")
            pass

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
            print("Unhandled Exception in recvJson: {}".format(e))
            raise e
        finally:
            # self.releaseLock("-recvJson-")
            pass

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
            print("Acquiring lock: {}".format(msg))
        self.L.acquire()
        if self.DEBUG_LOCK:
            print("Got       lock: {}".format(msg))

    def releaseLock(self, msg):
        if self.DEBUG_LOCK:
            print("Releasing lock: {}".format(msg))
        self.L.release()
        if self.DEBUG_LOCK:
            print("Free      lock: {}".format(msg))


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":
    print("Client->Server started. HOST:" + str(HOST) + " PORT:" + str(PORT_CLIENT_SERVER))
    server = SimpleServer((HOST, PORT_CLIENT_SERVER), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        # threading.Thread(target=server.serve_forever,daemon=True).start()
        server.serve_forever()
        print("Should Not see this.")
        while True:
            pass
            time.sleep(1)

    except KeyboardInterrupt:
        print("Main server interrupted.")

    finally:
        print("Finally closing server.")
        server.shutdown()
        server.server_close()

        GENERAL_EXIT_REQUEST = True
        # os.kill(os.getpid(),signal.SIGTERM) # send myself sigterm
