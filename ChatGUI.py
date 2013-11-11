"""
Chatroom client GUI


author: David Kale, Sina Tashakkori, Tim Jassman
version: 1
"""

import sys
from PyQt4 import QtGui, QtCore

class ChatRoom(QtGui.QWidget):
	
	userList = QtGui.QTextEdit("Users:")

	def __init__(self):
		super(ChatRoom, self).__init__()
		self.initUI()

	def initUI(self):
		# Displays the list of users
		#self.userList = QtGui.QTextEdit("Users:", self)
		#self.userList.setReadOnly(True)
		#self.userList.setFixedWidth(100)
		#self.userList.append("Timothy")
		#self.userList.append("David")
		#self.userList.append("Sina")
		userList.setReadOnly(True)
		userList.setFixedWidth(100)
		userList.append("Timothy")
		userList.append("David")
		userList.append("Sina")

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
		self.displayBox.addWidget(self.userList)
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
		if message:
			self.chatInput.clear()
			self.chatDisplay.append(message)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = ChatRoom()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()