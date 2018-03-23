import socket, threading, select, time, json, queue, traceback


class NackResponse(Exception):
    pass


class ClientHouse(object):
    __DEBUG_LOCK_ = True
    __DEBUG_SOCKETMSG_ = True
    __socket = None
    __server_addr = None
    __server_port = None
    __L = threading.Lock()
    __connected = False
    __client_name = None


    def __del__(self):
        print("Deleting ClientHouse..")

        if self.__socket:
            self.__socket.close()

        print("Delete ClientHouse completed.")

    def __init__(self, clientname, srv_addr, srv_port):
        self.__client_name = clientname
        self.__server_addr = srv_addr
        self.__server_port = srv_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__server_addr, self.__server_port))
            print("We are connected to the server. Sending HELLO..")
            ##now send hello msg
            data = {
                'msgtype': 'HELLO',
                'client_name': self.__client_name,
            }
            r = self.__send_dict_get_dict(data)
            self.assertACKmsg(r)
            print("Handshake was good. Ready to use clientHouse")
            self.__connected = True

        except Exception as e:
            print("\nException in init clientHouse\n")
            print(e)
            traceback.print_exc()
            self.__connected = False
            self.__del__()

    def __send_dict_get_dict(self, send_dict, buffersize=4096):

        self.acquireLock("SendDictGetDict")
        try:
            jsonstring = json.dumps(send_dict)
            encoded = jsonstring.encode("utf-8")
            self.__socket.sendall(encoded)
            if self.__DEBUG_SOCKETMSG_:
                print("#SCK Sent:   {}".format(encoded))
            byterecv = self.__socket.recv(buffersize)
            if not byterecv or byterecv == b'':
                raise Exception("Server closed?")
            dec = byterecv.decode("utf-8")
            if not dec or len(dec) < 5:
                raise Exception("Bad data decoded from server: {}".format(dec))
            if self.__DEBUG_SOCKETMSG_:
                print("#SCK Recv:   {}".format(dec))
            recv_dict = json.loads(dec)
            if not recv_dict or not recv_dict['msgtype']:
                raise Exception("Bad dict from server: {}".format(recv_dict))
            return recv_dict
        except Exception as e:
            print("\n__send_dict_get_dict exception\n")
            print(e)
            traceback.print_exc()
            self.__connected = False
            self.__del__()
        finally:
            self.releaseLock("SendDictGetDict")

    def requestClientsList(self):
        print("clientHouse requestClientsList")
        data = {'msgtype': 'LISTCLIENTS',
                'client_name': self.__client_name
                }
        try:
            msg = self.__send_dict_get_dict(data)
            if msg['msgtype'] != "SRVRESPONSE_CLIENTS":
                raise Exception("Bad clients response from server: {}".format(msg))
            list_clients = msg['clients']
            if not list_clients or len(list_clients) < 1:
                raise Exception("Bad list clients from server: {}".format(msg))
            return list_clients
        except Exception as e:
            print("\nrequestClientsList exception\n")
            print(e)
            traceback.print_exc()
            self.__connected = False
        finally:
            pass

    def requestClientMsgs(self):

        print("clientHouse requestClientMsgs")
        data = {'msgtype': 'GETALLMSGFORME',
                'client_name': self.__client_name
                }
        try:
            msg = self.__send_dict_get_dict(data)
            if msg['msgtype'] != "SRVRESPONSE_MSG":
                raise Exception("Bad msgs response from server: {}".format(msg))
            c = int(msg['count'])
            if c == 0:
                return c, []
            ll = msg['msgs']
            if not ll:
                raise Exception("List  msgs bad from server: {}".format(msg))
            if c != len(ll):
                raise Exception("Count msg and list msg size from server: {}".format(msg))
            return c, ll
        except Exception as e:
            print("\nrequestClientMsgs exception\n")
            print(e)
            traceback.print_exc()
            self.__connected = False
        finally:
            pass

    def sendCmdToClient(self, for_client, cmd, params):
        if not for_client or len(for_client) < 2 or not cmd or len(cmd) < 2:
            raise Exception("send cmd to client, bad parameters")
        a = {}
        for i in range(len(params)):
            a.update({'param' + str(i): params[i]})

        data = {'msgtype': 'COMMAND',
                'command': cmd,
                'client_name': self.__client_name,
                'for_client': for_client
                }
        data.update(a)
        r = self.__send_dict_get_dict(data)
        self.assertACKmsg(r)
        return

    def acquireLock(self, func):
        if self.__DEBUG_LOCK_:
            print("\nAcquiring lock from:{}".format(func))
        self.__L.acquire()
        if self.__DEBUG_LOCK_:
            print("\nAcquired lock from:{}".format(func))

    def releaseLock(self, func):
        if self.__DEBUG_LOCK_:
            print("\nReleasing lock from:{}".format(func))
        self.__L.release()
        if self.__DEBUG_LOCK_:
            print("\nReleased lock from:{}".format(func))

    def assertACKmsg(selfself, msg):
        if msg['msgtype'] == "ACK":
            return
        elif msg['msgtype'] == "NACK":
            raise NackResponse("\nNACK from server. Reason:   {}\n".format(msg['reason']))
        else:
            raise Exception("\n\nUnknown response type:  {}\n\n".format(msg))

    def isConnected(self):
        return bool(self.__connected)
