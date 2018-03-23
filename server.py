
import socketserver, subprocess, sys,socket,queue,threading,select,signal,os,time
from threading import Thread
from pprint import pprint
import json

KILL_COND=False
HOST = socket.gethostname()
PORT_CLIENT_SERVER = 9500




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
            
class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    pseudo_name=None
    DEBUG_LOCK=True
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
                                
                
                if(data):
                    print("We have indeed some data on socket")
                    text = data.decode('utf-8')
                    msg=json.loads(text);
                    if not msg:
                            raise ClientProblem("Malformed client message. Closing.")        
                    pprint(msg)       
                    self.handleClientMessage(msg)   
                self.L.release()

                if KILL_COND:
                   raise Exception("KILL_COND: General exit request, closing")
                    
        except ClientProblem as e:
            print("Client:"+str(self.client_address)+" disconnect.Bye!")
        except Exception as e:
            print("unhandled exception in SingleTCPRequest e:"+str(e))
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

     
                     
     def sendJson(self,data):
             #self.acquireLock("-sendJson-")
             try:
                    if not data or not data['msgtype']:
                            raise Exception("Malformed data to send in socket")
                    msg=json.dumps(data)
                    if not msg:
                            raise Exception("Cant convert data to json for send in socket")
                    self.request.send(msg.encode('utf-8'))
             except Exception as e:
                     print("Exception in sendJson: {}".format(e))
             finally:
                     #self.releaseLock("-sendJson-")
                     pass
                
     def recvJson(self,data,buffersize=4096):
             #self.acquireLock("-recvJson-")
             try:
                    data = self.request.recv(buffersize) 
                    if data==b'':
                            raise ClientProblem("client disconnect?")
                    if not data:
                            raise ClientProblem("Nod data from client")
                    text = data.decode('utf-8')
                    msg=json.loads(text);
                    
             except Exception as e:
                     print("Exception in recvJson: {}".format(e))
             finally:
                     #self.releaseLock("-recvJson-")
                     pass
                
     def createAckDict(self):
             data = {
                      'msgtype': 'ACK'                   
                    }
             return data
     def createNackDict(self):
             data = {
                      'msgtype': 'NACK'                   
                    }
             return data



             
     def acquireLock(self,msg):
             if self.DEBUG_LOCK:
                     print("Acquiring lock: {}".format(msg))
             self.L.acquire()
             if self.DEBUG_LOCK:
                     print("Got       lock: {}".format(msg))
     def releaseLock(self,msg):
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
    print("Client->Server started. HOST:"+str(HOST)+" PORT:"+str(PORT_CLIENT_SERVER))
    server = SimpleServer((HOST, PORT_CLIENT_SERVER), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        #threading.Thread(target=server.serve_forever,daemon=True).start()
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
       
        GENERAL_EXIT_REQUEST=True
        #os.kill(os.getpid(),signal.SIGTERM) # send myself sigterm
