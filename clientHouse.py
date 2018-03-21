import socket,threading,select,time,json,queue
KILL_PLS=False
class ServerListeningSynchroThread (threading.Thread):
    def __init__(self, client):
          threading.Thread.__init__(self)
          self.client=client
    def run(self):
          print ("Starting listen thread:" + self.name)
          try:
            while True:
                if KILL_PLS:
                    print("{} dead.".format(self.name))
                    return
                data=None
                #print("1Acquire")
                self.client.L.acquire()
                print("1acquired")
                ready = select.select([self.client.socket], [], [], 1)
                #print("1releasing")
                self.client.L.release()
                print("1released")
                if ready[0]:
                         print("Data in socket ready, lets get it!")
                         data = self.recvCmdAndACK()  
                if data==b'':
                    raise Exception("server disconnect?")
                if(data):
                    print("We have indeed some data on socket from server! Process it!")
                    self.processDataFromServer(data)
                
                    
          except Exception as e:
            print(e)

    def processDataFromServer(self,data):
        print("Data to process:  {} ....Adding to external queue...".format(data))
        self.client.queue.put(data)
        
    
    def recvCmdAndACK(self):
    #print("2Acquire")
        self.client.L.acquire()
        #print("2acquired")
        received = str(self.client.socket.recv(2048), "utf-8")
        print("Received: {}".format(received))
        self.client.socket.sendall(bytes("ACK" + "\n", "utf-8"))
        #print("2releasing")
        self.client.L.release()
        #print("2released")
        return received
    
class ClientHouse(object):
    socket=None
    queue=None
    server_addr=None
    server_port=None
    L=threading.Lock()
    thread=None
    def __del__(self):
        print("Deleting ClientHouse..")
        KILL_PLS=True
        if self.socket:
                self.socket.close()
        
       
        if self.thread:
                self.thread.join()
        self.L.release()        
        print("Delete ClientHouse completed.")
    
    def __init__(self,clientname, queue,saddr,sport):
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
           self.thread=ServerListeningSynchroThread(self)
           self.thread.start() 
        finally:
            print("init client done.")
           
            
    def SendJsonWaitResponse(self,data):
        print("SendJsonWaitResponse")
        message=json.dumps(data)
       # print("3Acquire")
        self.L.acquire()
       # print("3acquired")
        self.socket.sendall(bytes(message + "\n", "utf-8"))
        print("Sent:     {}".format(message))
        received = str(self.socket.recv(2048), "utf-8")
       # print("3releasing")
        self.L.release()
       # print("3released")
        print("Received: {}".format(received))
        return received 
 
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
