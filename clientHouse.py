import socket,threading,select,time,json,queue

class ServerListeningThread (threading.Thread):
    __socket=None
    client=None
    def __init__(self, client):
          threading.Thread.__init__(self)
          self.client=client
            
    def run(self):
          print ("Starting server listening thread:" + self.name)
          self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.__socket.connect((self.client.server_addr,self.client.server_to_client_port))
          print("We are connected to server for the reverse communication! Server:{} Port:{}".format(self.client.server_addr,str(self.client.server_to_client_port)))
          print("\nSending My Name to server->client socket")
          self.__socket.sendall(bytes( self.client.client_name, "utf-8"))
          received = str(self.__socket.recv(4096), "utf-8")
          print("\nServer says: {}".format(received))

          try:
            while True:
                if self.client.KILL_PLS:
                    print("{} dead.".format(self.name))
                    return
                data=None
                #self.client.acquireLock("ServerListeningSynchroThread Loop")
                
                ready=select.select([self.__socket],[],[],2)
                if ready[0]:
                    print("Data in socket ready, lets get it!")
                    data = self.recvCmdAndACK()
                

                    if data==b'':
                         raise Exception("server disconnect?")
                    if(data):
                            #print("We got something from server")
                         self.processDataFromServer(data)

               # self.client.releaseLock("ServerListeningSynchroThread Loop")
               # time.sleep(2)
                    
          except Exception as e:
            print(e)
          finally:
             # self.client.releaseLock("ServerListeningSynchroThread Loop")
             pass

    def processDataFromServer(self,data):
        print("Data to process:  {} ....Adding to external queue...".format(data))
        self.client.queue.put(data)
        
    
    def recvCmdAndACK(self):
        received = str(self.__socket.recv(2048), "utf-8")
        print("\nSERVER-CLIENT   Received: {}".format(received))
        self.__socket.sendall(bytes("ACK" + "\n", "utf-8"))
        return received
    
class ClientHouse(object):
    DEBUG_LOCK=False
    socket=None
    queue=None
    server_addr=None
    server_port=None
    server_to_client_port=None
    __L=threading.Lock()
    thread=None
    connected=False
    KILL_PLS=False
    client_name=None

    
    def __del__(self):
        print("Deleting ClientHouse..")
        
        self.KILL_PLS=True
        if self.thread:
                self.thread.join()
        if self.socket:
                self.socket.close()
              
        print("Delete ClientHouse completed.")
    
    def __init__(self,clientname, queue,saddr,sport,sToCPort):
        self.server_to_client_port=sToCPort
        self.queue=queue
        self.client_name=clientname
        self.server_addr=saddr
        self.server_port=sport
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
           self.socket.connect((self.server_addr, self.server_port))
           ##now send hello msg
           data = {
                   'msgtype': 'HELLO',
                   'client_name': self.client_name,
                  }
           r=self.SendJsonWaitResponse(data)
           if r!="ACK":
                raise Exception("Hello msg went wrong.")       
           ##now start listening thread    
           self.thread=ServerListeningThread(self)
           self.thread.start()
           self.connected=True
           
        except Exception as e:
            print(e)
            self.connected=False
            
           
            
    def SendJsonWaitResponse(self,data):
        
        self.acquireLock("SendJsonWaitResponse")
        try:
            message=json.dumps(data)
            
            self.socket.sendall(bytes(message + "\n", "utf-8"))
            print("Sent:     {}".format(message))
            received = str(self.socket.recv(2048), "utf-8")      
            print("Received: {}".format(received))    
            return received
        except Exception as e:
            print(e)
            self.connected=False
        finally:
            self.releaseLock("SendJsonWaitResponse")

    def requestClientsList(self):
        data={'msgtype':'LISTCLIENTS',
          'client_name':self.client_name
        }
        self.acquireLock("requestClientsList")
        try:
            message=json.dumps(data)
            self.socket.sendall(bytes(message + "\n", "utf-8"))
            received = str(self.socket.recv(2048), "utf-8")
            if not received or len(received)<3:
                print("Bad clients , probably server was sending stuffs")
                return
            print("Clients Received: {}".format(received))
            msg=json.loads(received)
            if msg['msgtype']!="SRVRESPONSE_CLIENTS":
                print("This is not a clients response type")
                return
            return msg['clients']
        except Exception as e:
            print("requestClients exception")
            print(e)
            self.connected=False
        finally:
            self.releaseLock("requestClientsList")


    def acquireLock(self,func):
        if self.DEBUG_LOCK:
            print("\nAcquiring lock from:{}".format(func))
        self.__L.acquire()
        if self.DEBUG_LOCK:
            print("\nAcquired lock from:{}".format(func))

    def releaseLock(self,func):
        if self.DEBUG_LOCK:
            print("\nReleasing lock from:{}".format(func))
        self.__L.release()
        if self.DEBUG_LOCK:
            print("\nReleased lock from:{}".format(func))
        
    def sendCmdToClient(self,for_client,cmd,params):
        if not for_client or len(for_client)<2 or not cmd or len(cmd)<2:
            raise Exception("send cmd to client, bad parameters")
        a={}
        for i in range(len(params)):
            a.update({'param'+str(i):params[i]})
            
        data={'msgtype':'COMMAND',
          'command':cmd,
          'client_name':self.client_name,
          'for_client':for_client          
        }
        data.update(a)
        r=self.SendJsonWaitResponse(data)
        if r!="ACK":
             raise Exception("Sending cmd to client went wrong")
        return
