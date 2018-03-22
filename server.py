
import socketserver, subprocess, sys,socket,queue,threading,select,signal,os,time
from threading import Thread
from pprint import pprint
import json

class SingletonMixin(object):
        __singleton_lock = threading.Lock()
        __singleton_instance = None
        list_queue=[]
        @classmethod
        def instance(cls):
            if not cls.__singleton_instance:
                    with cls.__singleton_lock:
                        if not cls.__singleton_instance:
                            cls.__singleton_instance = cls()
            return cls.__singleton_instance
        def getQueueByName(self,name): 
            found=False;
            for i in range(len(self.list_queue)):
                thisq=self.list_queue[i]
                if thisq['Name']==name:
                    found=True
                    #print("Found queue for {}".format(name))
                    return thisq['q'];
            if len(self.list_queue)==0 or found==False:
                q=queue.Queue()
                
                self.list_queue.append({'Name':name,'q':q})
                print("Cant find queue for {}, creating new one.".format(name))
                return q;
            raise Exception("Really Dunno in getqueuebyname...")
        
        def destroyQueueByName(self,name):
            for i in range(len(self.list_queue)):
                thisq=self.list_queue[i]
                #print(thisq)
                if thisq['Name']==name:
                    print("found the list for name {}. List was size={}".format(name,len(self.list_queue)))
                    del self.list_queue[i]
                    print("now list size is:{}".format(len(self.list_queue)))
                    return
            print("Queue was not present for name:{},leaving as it was".format(name))

        def getAllQueueName(self):
                 l=[]
                 for i in range(len(self.list_queue)):
                        thisq=self.list_queue[i]
                        l.append(thisq['Name'])
                 return l
        

        
class ClientProblem(Exception):
    pass
HOST = socket.gethostname()
PORT_CLIENT_SERVER = 9500
PORT_SERVER_CLIENT = 9501

class ServerToClientThread(socketserver.BaseRequestHandler):
         client_name=None
         
         def handle(self):
                print("\n\n\n\n\nThread ServerToClientThread to serves addr:"+str(self.client_address))
          
                received = str(self.request.recv(2048), "utf-8")
  
                print("Client says : {}".format(received))
                self.request.sendall(bytes("Hi client.Welcome i will send here stuffs for sure!" + "\n", "utf-8"))
                self.name=received

                if not self.name or len(self.name)<4:
                        print("Wattafuck ho preso il nome ma non ho preso il nome !?!?!?")
                        return
                try:
                    while True:
                        
                        q=SingletonMixin.instance().getQueueByName(str(self.name))
                        if not q or q.empty():
                            continue

                        #print("we are about to get item")
                        e=q.get()
                        print("Item Got")
                        if not e:
                            print("daffaq?")
                            raise Exception("Daffq? got and element from queue but Null?!?!??")
                       
                        
                        while(e):
                                    msg=json.dumps(e)
                                    print("got element in queue for client{} msg:{} ....Sending to client".format(self.name,msg))
                                    
                                    self.request.sendall(bytes(msg + "\n", "utf-8"))
                                    data = self.request.recv(4096)
                                    
                                    if data==b'':
                                         raise ClientProblem("client disconnect?")
                                    text = data.decode('utf-8')
                                    print("Message back from client:{}".format(text))
                                    if not q.empty():
                                        e=q.get()
                                    else:
                                        e=None
                    
                     
                except ClientProblem as e:
                    print("Client:"+str(self.client_address)+" disconnect.Bye!")
                except Exception as e:
                    print("unhandled exception e:"+str(e))
                finally:
                    #self.KILL_MY_SON=True    
                    if self.name:
                       SingletonMixin.instance().destroyQueueByName(str(self.name))          
                    self.request.close()
                
class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    pseudo_name=None
    KILL_MY_SON=False
    L=threading.Lock()

    def handle(self):
        print("Thread spawned to serves addr:"+str(self.client_address))
        
        try:
            while True:
                data=None
                #print("ml acquiring..")
                self.L.acquire()
               # print("ml acquired..")
                ready = select.select([self.request], [], [], 1)
                if ready[0]:
                         data = self.request.recv(2048)       
                if data==b'':
                    raise ClientProblem("client disconnect?")
                if(data):
                    print("We have indeed some data on socket")
                    text = data.decode('utf-8')
                    msg=json.loads(text); 
                    pprint(msg)       
                    self.handleClientMessage(msg)   
                self.L.release()
                #print("ml released..")    
                #self.handleQueue()
                #if GENERAL_EXIT_REQUEST:
                #   raise Exception("General exit request, closing")
                    
        except ClientProblem as e:
            print("Client:"+str(self.client_address)+" disconnect.Bye!")
        except Exception as e:
            print("unhandled exception e:"+str(e))
        finally:
            #self.KILL_MY_SON=True    
            if self.pseudo_name:
               SingletonMixin.instance().destroyQueueByName(str(self.pseudo_name))          
            self.request.close()


                
    def handleClientMessage(self,msgDict):

        if msgDict['msgtype']=="HELLO":
            if self.pseudo_name!=None:
                raise Exception("Duplicate hello msg? oldname:"+self.pseudo_name)
            self.pseudo_name=msgDict['client_name']
            ##prob a work around, create queue now
            SingletonMixin.instance().getQueueByName(str(self.pseudo_name))
            print("Hello msg recv. Got client name:"+self.pseudo_name)
            self.request.send('ACK'.encode('utf-8'))
        else:
             if self.pseudo_name==None:
                 raise Exception("cant recv something before hello msg:"+str(msgDict))
             if msgDict['client_name']!=self.pseudo_name:
                 raise Exception("wtf? processing message not mine.:"+str(msgDict))
             if msgDict['msgtype']=="COMMAND":
                 print("we got a command: {} for client:{}".format(msgDict['command'],msgDict['for_client']))
                 q=SingletonMixin.instance().getQueueByName(str(msgDict['for_client']))
                 q.put(msgDict)
                 print("Added msg in queue for client:{}".format(msgDict['for_client']))
                 self.request.send('ACK'.encode('utf-8'))
                 return 
             if msgDict['msgtype']=="LISTCLIENTS":
                     l=SingletonMixin.instance().getAllQueueName()
                     data = {
                                   'msgtype': 'SRVRESPONSE_CLIENTS',
                                   'clients': l
                            }
                     msg=json.dumps(data)
                     self.request.send(msg.encode('utf-8'))
                     return
                     
        
class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

class ServerToClient(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    print("Client->Server started. HOST:"+str(HOST)+" PORT:"+str(PORT_CLIENT_SERVER))
    server = SimpleServer((HOST, PORT_CLIENT_SERVER), SingleTCPHandler)
    
    print("Server->Client started. HOST:"+str(HOST)+" PORT:"+str(PORT_SERVER_CLIENT))
    serverToclients=ServerToClient((HOST, PORT_SERVER_CLIENT), ServerToClientThread)
    # terminate with Ctrl-C
    try:
        threading.Thread(target=server.serve_forever,daemon=True).start()
        threading.Thread(target=serverToclients.serve_forever,daemon=True).start()
        
        print("All threads started.")
        while True:
               pass
               time.sleep(1)
        
    except KeyboardInterrupt: 
        print("Main server interrupted.")
        
    finally:
        print("ALLOROR? R?Q?AS?AS?AS?")
        server.shutdown()
        server.server_close()
        serverToclients.shutdown()
        serverToclients.server_close()
        GENERAL_EXIT_REQUEST=True
        os.kill(os.getpid(),signal.SIGTERM) # send myself sigterm
