import os
import sys
import time
import datetime
def setShutdown(seconds):
  cmdString="shutdown -s -t {0}".format(seconds)
  r=os.system(cmdString)
  if r!=0:
    print("WARNING:System shutdown was already planned. Overwriting..")
    os.system("shutdown -a")
    r=os.system(cmdString)
    if r!=0:
      print("ERROR : Hard fail not able to overwrite pending operation, let's stop everything..")
      sys.exit(1)
  return
printstamp=0
timewillshutdown=0;
while True:
  print("\n1 - Stop pending shutdown\n2 - Shutdown in 30 mins\n3 - Shutdown in 60 mins\n4 - Status\n5 - Exit")
  opt=input("Option?")
  opt=int(opt)
  print("\n")
  if opt==1:
    r=os.system("shutdown -a")
    if r!=0:
        print("Shutdown was not pending")
    else:
         print("Shutdown Halted.")
    printstamp=0
    continue
  elif opt==2:
    setShutdown(1800)
    printstamp=time.time()
    timewillshutdown=printstamp+1800
    print("System will be shutdown in 30 mins")
    continue
  elif opt==3:
    setShutdown(3600)
    printstamp=time.time()
    timewillshutdown=printstamp+3600
    print("System will be shutdown in 60 mins")
    continue
    
  elif opt==4:
    if printstamp==0:
        print("Nothing pending.")
    else:
        left_Seconds=int(timewillshutdown-time.time())
        left=str(datetime.timedelta(seconds=left_Seconds))
        print("System will be shutdown in "+left)
        continue;
  elif opt==5:
    print("Leaving as it is. Bye :)")
    sys.exit(0)
  else:
    continue
    

