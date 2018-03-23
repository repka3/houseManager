from clientHouse import ClientHouse
import time,traceback
cond=True
while (cond):
    try:
        clientHouse = ClientHouse("C1", "DESKTOP-TTCCQR0", 9500)
        while clientHouse.isConnected():
            clientHouse.requestClientsList()
            time.sleep(1)

    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        cond=True
        print("finally")



