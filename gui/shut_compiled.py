# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shutdown.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 643)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1050, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(690, 480, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(325, 545, 196, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(445, 15, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(405, 50, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(445, 50, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_status.setFont(font)
        self.label_status.setObjectName("label_status")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(535, 45, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 15, 266, 516))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_timer = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_timer.setFont(font)
        self.label_timer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_timer.setObjectName("label_timer")
        self.horizontalLayout_2.addWidget(self.label_timer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_stop = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.verticalLayout.addWidget(self.pushButton_stop)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_minShutdown = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_minShutdown.sizePolicy().hasHeightForWidth())
        self.pushButton_minShutdown.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_minShutdown.setFont(font)
        self.pushButton_minShutdown.setObjectName("pushButton_minShutdown")
        self.horizontalLayout.addWidget(self.pushButton_minShutdown)
        self.lineEdit_shutdownTime = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_shutdownTime.sizePolicy().hasHeightForWidth())
        self.lineEdit_shutdownTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_shutdownTime.setFont(font)
        self.lineEdit_shutdownTime.setObjectName("lineEdit_shutdownTime")
        self.horizontalLayout.addWidget(self.lineEdit_shutdownTime)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_30 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_30.setFont(font)
        self.pushButton_30.setObjectName("pushButton_30")
        self.verticalLayout.addWidget(self.pushButton_30)
        self.pushButton_60 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_60.setFont(font)
        self.pushButton_60.setObjectName("pushButton_60")
        self.verticalLayout.addWidget(self.pushButton_60)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(300, 100, 706, 336))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.listView_clients = QtWidgets.QListView(self.formLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_clients.sizePolicy().hasHeightForWidth())
        self.listView_clients.setSizePolicy(sizePolicy)
        self.listView_clients.setObjectName("listView_clients")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.listView_clients)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_remote_sd_custom = QtWidgets.QPushButton(self.formLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remote_sd_custom.sizePolicy().hasHeightForWidth())
        self.pushButton_remote_sd_custom.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_remote_sd_custom.setFont(font)
        self.pushButton_remote_sd_custom.setObjectName("pushButton_remote_sd_custom")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_remote_sd_custom)
        self.pushButton_remote_sd_now = QtWidgets.QPushButton(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_remote_sd_now.setFont(font)
        self.pushButton_remote_sd_now.setObjectName("pushButton_remote_sd_now")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pushButton_remote_sd_now)
        self.pushButton_remote_sd_stop = QtWidgets.QPushButton(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_remote_sd_stop.setFont(font)
        self.pushButton_remote_sd_stop.setObjectName("pushButton_remote_sd_stop")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButton_remote_sd_stop)
        self.lineEdit_remote_time = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_remote_time.sizePolicy().hasHeightForWidth())
        self.lineEdit_remote_time.setSizePolicy(sizePolicy)
        self.lineEdit_remote_time.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_remote_time.setFont(font)
        self.lineEdit_remote_time.setObjectName("lineEdit_remote_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_remote_time)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.formLayout)
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(679, 10, 291, 76))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.lineEdit_clientName = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_clientName.sizePolicy().hasHeightForWidth())
        self.lineEdit_clientName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.lineEdit_clientName.setFont(font)
        self.lineEdit_clientName.setObjectName("lineEdit_clientName")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_clientName)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_serveraddr = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_serveraddr.sizePolicy().hasHeightForWidth())
        self.lineEdit_serveraddr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_serveraddr.setFont(font)
        self.lineEdit_serveraddr.setObjectName("lineEdit_serveraddr")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_serveraddr)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(290, 55, 10, 381))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_exit.setText(_translate("MainWindow", "Exit !"))
        self.label_4.setText(_translate("MainWindow", "by Luna per l\'amore !"))
        self.label.setText(_translate("MainWindow", "Network"))
        self.label_5.setText(_translate("MainWindow", "Status:"))
        self.label_status.setText(_translate("MainWindow", "Disconnected"))
        self.pushButton_connect.setText(_translate("MainWindow", "Connect!"))
        self.label_7.setText(_translate("MainWindow", "Locale"))
        self.label_3.setText(_translate("MainWindow", "Shutdown in"))
        self.label_timer.setText(_translate("MainWindow", "00:00:00"))
        self.pushButton_stop.setText(_translate("MainWindow", "Stop pending operation!"))
        self.pushButton_minShutdown.setText(_translate("MainWindow", "ShutDown in (min)"))
        self.lineEdit_shutdownTime.setText(_translate("MainWindow", "45"))
        self.pushButton_30.setText(_translate("MainWindow", "ShutDown in 30 min !"))
        self.pushButton_60.setText(_translate("MainWindow", "ShutDown in 60 min !"))
        self.pushButton_remote_sd_custom.setText(_translate("MainWindow", "ShutDown in (min)"))
        self.pushButton_remote_sd_now.setText(_translate("MainWindow", "ShutDown Now!"))
        self.pushButton_remote_sd_stop.setText(_translate("MainWindow", "Stop pending operation"))
        self.lineEdit_remote_time.setText(_translate("MainWindow", "45"))
        self.lineEdit_clientName.setText(_translate("MainWindow", "DESKTOP-ALE"))
        self.label_2.setText(_translate("MainWindow", "Server addr"))
        self.lineEdit_serveraddr.setText(_translate("MainWindow", "DESKTOP-TTCCQR0"))
        self.label_6.setText(_translate("MainWindow", "Client name"))

