from PyQt5 import QtCore, QtGui, QtWidgets
from shut_compiled import Ui_MainWindow
import sys
class MyFirstGuiProgram(Ui_MainWindow):
	def __init__(self, dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
 
		# Connect "add" button with a custom function (addInputTextToListbox)
		#self.addBtn.clicked.connect(self.addInputTextToListbox)
 
	#def addInputTextToListbox(self):
	#	txt = self.myTextInput.text()
	#	self.listWidget.addItem(txt)
 
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()
 
	prog = MyFirstGuiProgram(window)
 
	window.show()
	sys.exit(app.exec_())

