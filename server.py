
import socketserver, subprocess, sys,socket,queue,threading,select,signal,os
from threading import Thread
from pprint import pprint
import json

GENERAL_EXIT_REQUEST=False

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
            
class ClientProblem(Exception):
    pass
HOST = socket.gethostname()
PORT = 9500

class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    pseudo_name=None
    def handle(self):
        print("Thread spawned to serves addr:"+str(self.client_address))
        
        try:
            while True:
                data=None
                ready = select.select([self.request], [], [], 2)
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
                    self.request.send('ACK'.encode('utf-8'))
                self.handleQueue()
                if GENERAL_EXIT_REQUEST:
                    raise Exception("General exit request, closing")
                    
        except ClientProblem as e:
            print("Client:"+str(self.client_address)+" disconnect.Bye!")
        except Exception as e:
            print("unhandled exception e:"+str(e))
        finally:
            if self.pseudo_name:
               SingletonMixin.instance().destroyQueueByName(str(self.pseudo_name))          
            self.request.close()

    def handleQueue(self):
        #print("handlequeue {}".format(self.pseudo_name))
        q=SingletonMixin.instance().getQueueByName(str(self.pseudo_name))
        if not q or q.empty():
            return
        
        e=q.get()
        if not e:
            print("daffaq?")
            raise Exception("Daffq? got and element from queue but Null?!?!??")
        while(e):
            msg=json.dumps(e)
            print("got element in queue for client{} msg:{} ....Sending to client".format(self.pseudo_name,msg))
            self.request.sendall(bytes(msg + "\n", "utf-8"))
            data = self.request.recv(2048)       
            if data==b'':
                 raise ClientProblem("client disconnect?")
            text = data.decode('utf-8')
            print("Message back from client:{}".format(text))
            if not q.empty():
                e=q.get()
            else:
                e=None
  
        print("Processing queue for client:{} done.".format(self.pseudo_name))
        
                
    def handleClientMessage(self,msgDict):

        if msgDict['msgtype']=="HELLO":
            if self.pseudo_name!=None:
                raise Exception("Duplicate hello msg? oldname:"+self.pseudo_name)
            self.pseudo_name=msgDict['client_name']
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
                 return 
            
        
class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    print("Server started HOST:"+str(HOST)+" PORT:"+str(PORT))
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt: 
        print("Main server interrupted.")
        
    finally:
        print("ALLOROR? R?Q?AS?AS?AS?")
        server.shutdown()
        server.server_close()
        GENERAL_EXIT_REQUEST=True
        #os.kill(os.getpid(),signal.SIGTERM) # send myself sigterm
