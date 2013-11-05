"""
Chatroom client GUI


author: David Kale, Sina Tashakkori, Tim Jassman
version: 1
"""

import sys
from PyQt4 import QtGui

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.initUI()

	def initUI(self):
		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle("Chatroom")
		self.setWindowIcon(QtGui.QIcon('icons\sina.png'))
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()