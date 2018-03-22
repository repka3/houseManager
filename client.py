from clientHouse import ClientHouse 
import queue,time,_thread,traceback


def loopLookQueueMsg(q):
    while True:
        item=q.get()
        print("GOT NEW MESSAGE FOR US!  msg:{}".format(item))


HOST="DESKTOP-TTCCQR0"
CLIENT_NAME="NOTEBOOK-IRENE"
PORT=9500
q=queue.Queue()
client=None
try:
    client=ClientHouse(CLIENT_NAME,q,HOST,PORT)
    #_thread.start_new_thread( loopLookQueueMsg, (q, ) )
    remoteclients=client.requestClientsList()
    print("Clients:  {}".format(remoteclients))
    time.sleep(3)
    client.sendCmdToClient(CLIENT_NAME,"shutdown",(1800,))
    
        

except Exception as e:
    print(e)
    traceback.print_exc()
finally:
    if client:
        print("LOLOL DELETING CLIENT")
        client.__del__()
    print("potta")

