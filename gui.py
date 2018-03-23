from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from shut_compiled import Ui_MainWindow
import sys, queue, threading, time, os, datetime, json, traceback
from clientHouse import ClientHouse


class LoopThread(threading.Thread):
    gui = None
    count = 0

    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui

    def run(self):
        try:
            print("Starting loop thread")
            self.count = 0
            while True:
                if self.gui.KILL_PLS:
                    return
                time.sleep(1)
                self.gui.refreshTimerLaber()

                if self.gui.clientHouse and self.gui.clientHouse.isConnected():
                    print("We are connected to server.")
                    self.gui.label_status.setText("Connected")
                    self.gui.label_status.setStyleSheet(("QLabel {  color : gree; }"))
                    if self.count % 2 == 0:
                        self.gui.updateClientList()
                    else:
                        self.gui.updateMessages()

                else:
                    print("Disconnected from server.")
                    self.gui.label_status.setText("Disconnected")
                    self.gui.label_status.setStyleSheet(("QLabel {  color : red; }"))

                self.count = self.count + 1
                if self.count > 1000:
                    self.count = 0

        except Exception as e:
            print(e)
        finally:
            print("\nThread loop dead\n")


class MyFirstGuiProgram(Ui_MainWindow):
    PORT = 9500
    clientHouse = None
    client_name = None
    q = queue.Queue()
    model = None
    selectmodel = None
    loopthread = None
    KILL_PLS = None
    timewillshutdown = -1
    connected_to_server = False
    lastClientNameSelected = None
    oldClients = []

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.pushButton_connect.clicked.connect(self.ConnectServer)
        # self.ui.closeEvent = self.closeEvent
        window.closeEvent = self.closeEvent
        self.model = QtGui.QStandardItemModel(self.listView_clients)
        self.listView_clients.setModel(self.model)
        self.selectmodel = QtCore.QItemSelectionModel()
        self.selectmodel.flags = QtCore.QItemSelectionModel.ClearAndSelect
        self.listView_clients.setSelectionModel(self.selectmodel)
        self.listView_clients.selectionModel().selectionChanged.connect(self.selectClientChanges)

        # adjust sizes
        '''
        self.pushButton_30.adjustSize()
        self.pushButton_60.adjustSize()
        self.pushButton_connect.adjustSize()
        self.pushButton_minShutdown.adjustSize()
        self.pushButton_refresh_clients.adjustSize()
        self.pushButton_stop.adjustSize()
        self.pushButton_remote_sd_custom.adjustSize()
        self.pushButton_remote_sd_now.adjustSize()
        self.pushButton_remote_sd_stop.adjustSize()
        '''
        sett=self.tryLoadSettings()
        self.lineEdit_clientName.setText(str(sett).strip())
        self.lineEdit_clientName.returnPressed.connect(self.writeSettings)

        print(sett)
        # handle close application
        self.pushButton_exit.clicked.connect(self.SafeCleanUp)

        self.label_status.setText("Disconnected")
        self.label_status.setStyleSheet(("QLabel {  color : red; }"))

        # local buttons
        self.pushButton_30.clicked.connect(lambda: self.setLocalShutDown(30 * 60))
        self.pushButton_60.clicked.connect(lambda: self.setLocalShutDown(60 * 60))
        self.pushButton_minShutdown.clicked.connect(lambda: self.setLocalShutDown(-1))
        self.pushButton_stop.clicked.connect(self.stopPendingShutdown)

        # remote buttons
        self.pushButton_remote_sd_now.clicked.connect(lambda: self.sendRemoteShutdown(0))
        self.pushButton_remote_sd_custom.clicked.connect(lambda: self.sendRemoteShutdown(-1))
        self.pushButton_remote_sd_stop.clicked.connect(self.sendRemotestopPending)

        # Loop thread
        self.loopthread = LoopThread(self)
        self.loopthread.start()

        # just to be safe
        r = os.system("shutdown -a")
        if r == 0:
            self.displayInfoBox("Im sorry. I had to stop scheduled operation.")

        # remote clients buttons
        self.enableRemoteClientCommands(False)

    def tryLoadSettings(self):
        if os.path.exists("sett.ini"):
            with open('sett.ini', 'r') as file:
                for line in file:
                    file.close()
                    return line.strip()
        else:
            with open('sett.ini', 'w') as file:
                file.write("NomeClient")
                file.close()
                return "NomeClient"

    def writeSettings(self):
        print("Write new client sett")
        setta = self.lineEdit_clientName.text()
        print(setta)
        sett = str(setta).strip()
        print(setta)
        with open('sett.ini', 'w') as file:
            file.write(sett)
            file.close()

    def displayInfoBox(self, msg):
        box = QtWidgets.QMessageBox()
        box.setWindowTitle("Information")
        box.setIcon(QtWidgets.QMessageBox.Information)
        box.setText(msg)
        box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        box.exec()
        return

    def enableRemoteClientCommands(self, enable):
        self.pushButton_remote_sd_custom.setEnabled(enable)
        self.pushButton_remote_sd_now.setEnabled(enable)
        self.pushButton_remote_sd_stop.setEnabled(enable)

    def selectClientChanges(self):
        print("selection changes")
        selects = self.listView_clients.selectedIndexes()
        # print(selects)
        if len(selects) > 1:
            raise Exception("more then one client selected??")
        # print("trollo2")

        it = selects[0]
        item = self.model.itemFromIndex(it)
        self.lastClientNameSelected = item.text()
        print("Client selected:{}".format(self.lastClientNameSelected))
        '''
        #print("trollo3")
        lab=it.data()
        print(lab)
        self.lastClientNameSelected=lab
        #print(self.lastClientNameSelected)
        '''
        self.enableRemoteClientCommands(True)

    def SafeCleanUp(self):
        print("Safe cleanup starting...")
        self.KILL_PLS = True
        if self.loopthread:
            print("Loop Thread killing....")
            self.loopthread.join()
            print("Loop Thread kill done.")

        if self.clientHouse:
            print("Killing clientHouse.__del__()")
            self.clientHouse.__del__()
        print("Safe cleanup done.")
        sys.exit(0)


    def closeEvent(self, event):
        self.SafeCleanUp()
        event.accept()


    def updateMessages(self):
        print("Updating messages through clientHouse")
        c, msgs = self.clientHouse.requestClientMsgs()
        if c == 0:
            print("No messages to process.")
            return
        for m in msgs:
            self.processRemoteCommand(m)


    def updateClientList(self):
        print("Requesting clients through clientHouse")
        remoteclients = self.clientHouse.requestClientsList()
        NeedRefresh = True
        if not remoteclients:
            print("probably bad clients response so, just ignore it")
            return
        # check if we need to update GUI
        if self.oldClients and len(self.oldClients) > 0:
            for c in remoteclients:
                if c in self.oldClients:
                    NeedRefresh = False
                else:
                    NeedRefresh = True
                    break

        if NeedRefresh:
            self.oldClients = remoteclients
            print("Clients list changed.Updating ListView with clients")
            self.setClientsList(remoteclients)


    def ConnectServer(self):
        try:
            if self.clientHouse:
                self.clientHouse.__del__()

            addr = self.lineEdit_serveraddr.text()
            client_name = self.lineEdit_clientName.text()
            if not addr or len(addr) < 2 or not client_name or len(client_name) < 2:
                print("not valid params connection")
                return
            self.client_name = client_name
            self.clientHouse = ClientHouse(self.client_name, addr, int(self.PORT))

        except Exception as e:
            print("\n\nConnect to server exception.\n")
            print(e)
            traceback.print_exc()
            if self.clientHouse:
                self.clientHouse.__del__()
                self.clientHouse = None
        finally:
            pass


    def sendRemotestopPending(self):
        if not self.lastClientNameSelected:
            print("No client selected")
            return
        self.clientHouse.sendCmdToClient(self.lastClientNameSelected, "stoppending", ())


    def sendRemoteShutdown(self, delasec):
        if not self.lastClientNameSelected:
            print("No client selected")
            return
        if delasec == -1:
            customtime = self.lineEdit_remote_time.text()
            if len(customtime) < 1:
                return
            t = int(customtime)
            if t < 1:
                return
            delasec = t * 60

        self.clientHouse.sendCmdToClient(self.lastClientNameSelected, "shutdown", (delasec,))


    def processRemoteCommand(self, msg):
        if msg['for_client'] != self.client_name:
            raise Exception("\nWATTTTAAAA\n ARE WE PROCESSING SOMETHING FOR ANOTHER ONE?!?!?!?!?!?!?!\n\n\n")

        if msg['msgtype'] == "COMMAND" and msg['command'] == "shutdown":
            delas = int(msg['param0'])
            if delas < 0:
                print("Bad param0 for shutdown?")
                return
            self.setLocalShutDown(delas)
        elif msg['msgtype'] == "COMMAND" and msg['command'] == "stoppending":
            self.stopPendingShutdown()
        else:
            print("\n\n\nWARN: I dont know how to process this message: {}\n\n\n".format(msg))


    def stopPendingShutdown(self):
        r = os.system("shutdown -a")
        if r != 0:
            print("Shutdown was not pending")
        self.timewillshutdown = -1


    def setLocalShutDown(self, delasec):
        if not delasec:
            return
        if delasec == -1:
            customtime = self.lineEdit_shutdownTime.text()
            if len(customtime) < 1:
                return
            t = int(customtime)
            if t < 1:
                return
            delasec = t * 60

        cmdString = "shutdown -s -t {0}".format(delasec)
        r = os.system(cmdString)
        if r != 0:
            print("WARNING:System shutdown was already planned. Overwriting..")
            os.system("shutdown -a")
            r = os.system(cmdString)
            if r != 0:
                print("ERROR : Hard fail not able to overwrite pending operation, let's stop everything..")
                sys.exit(1)
        print("system will be shutdown in {} seconds".format(delasec))
        printstamp = time.time()
        self.timewillshutdown = printstamp + delasec
        self.refreshTimerLaber()
        return


    def refreshTimerLaber(self):
        if (self.timewillshutdown < 0):
            self.label_timer.setText("Nothing scheduled :)")
            return
        left_Seconds = int(self.timewillshutdown - time.time())
        left = str(datetime.timedelta(seconds=left_Seconds))
        self.label_timer.setText(left)


    def setSelectedClientByLastClientorClear(self):
        print("setSelectedClientByLastClientorClear")
        if not self.lastClientNameSelected:
            print("lastClient Not set")
            return

        l_item = self.model.findItems(self.lastClientNameSelected, Qt.Qt.MatchFixedString)

        if not l_item or len(l_item) != 1:
            print("list l_item not valid or more then one with same name in the list?!")
            return

        l_qindex = self.model.indexFromItem(l_item[0])
        if not l_qindex:
            print(" qindex not valid or more then one with same name in the list?!")
            return
        self.listView_clients.selectionModel().select(l_qindex, QtCore.QItemSelectionModel.ClearAndSelect)
        selects = self.listView_clients.selectedIndexes()
        print(selects)
        if len(selects) > 1:
            raise Exception("more then one client selected??")

        it = selects[0]
        item = self.model.itemFromIndex(it)
        print("Item selected text:{}".format(item.text()))


    def setClientsList(self, l):
        self.model.removeRows(0, self.model.rowCount())

        for i in range(len(l)):
            c = l[i]
            it = QtGui.QStandardItem()
            it.setText(c)
            it.setSelectable(True)
            self.model.appendRow(it)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(window)

    window.show()
    sys.exit(app.exec_())
