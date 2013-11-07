"""
Chatroom client GUI


author: David Kale, Sina Tashakkori, Tim Jassman
version: 1
"""

import sys
from PyQt4 import QtGui, QtCore

class ChatRoom(QtGui.QWidget):
	
	def __init__(self):
		super(ChatRoom, self).__init__()
		self.initUI()

	def initUI(self):
		# Displays the list of users
		self.userDisplay = QtGui.QTextEdit("Users:", self)
		self.userDisplay.setReadOnly(True)
		self.userDisplay.setFixedWidth(100)
		self.userDisplay.append("Timothy")
		self.userDisplay.append("David")
		self.userDisplay.append("Sina")

		# Displays the chat
		self.chatDisplay = QtGui.QTextEdit(self)
		self.chatDisplay.setReadOnly(True)
		self.chatDisplay.append("Test")
		self.chatDisplay.append("Test2")

		# Text input for chat
		self.chatInput = QtGui.QLineEdit(self)
		
		# Button to send chat message
		self.sendButton = QtGui.QPushButton('Send', self)
		self.sendButton.clicked.connect(self.sendmessage)
		
		# Layout management
		self.displayBox = QtGui.QHBoxLayout()
		self.displayBox.addWidget(self.chatDisplay)
		self.displayBox.addWidget(self.userDisplay)
		self.sendBox = QtGui.QHBoxLayout()
		self.sendBox.addWidget(self.chatInput)
		self.sendBox.addWidget(self.sendButton)
		self.container = QtGui.QVBoxLayout(self)
		self.container.addLayout(self.displayBox)
		self.container.addLayout(self.sendBox)

		self.setLayout(self.container)

		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle("Chatroom")
		self.setWindowIcon(QtGui.QIcon("icons\sina.png"))
		self.show()

	def PASScloseEvent(self, event):
		reply = QtGui.QMessageBox.question(self, "Message", 
			"Are you sure you want to quit?", QtGui.QMessageBox.Yes |
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def sendmessage(self):
		message = self.chatInput.text()
		self.chatInput.clear()
		self.chatDisplay.append(message)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = ChatRoom()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()