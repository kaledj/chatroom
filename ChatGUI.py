#!/usr/bin/python

"""
ChatGUI.py: Defines a python class that implements a GUI for the chatroom. 
			Utilizes PyQt4 for GUI components.

author: David Kale, Sina Tashakkori, Tim Jassmann
version: 1
"""

import sys
from PyQt4 import QtGui, QtCore

class ChatGUI(QtGui.QWidget):
	
	# Constructor
	#
	def __init__(self):
		super(ChatGUI, self).__init__()
		self.initUI()

	#  initUI - Method that creates GUI components in the proper order, 
	#			sets the desired measurements for those components, 
	#           puts the components together, and then makes them 
	#			visible to the user.
	#
	def initUI(self):
		# Displays the list of users
		self.userList = QtGui.QTextEdit("Users:", self)
		self.userList.setReadOnly(True)
		self.userList.setFixedWidth(100)

		# Displays the chat log
		self.chatDisplay = QtGui.QTextEdit(self)
		self.chatDisplay.setReadOnly(True)

		# Text input for chat
		self.chatInput = QtGui.QLineEdit(self)
		self.chatInput.setMaxLength(100)

		# Button to send chat message
		self.sendButton = QtGui.QPushButton('Send', self)
		
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

		# Display the window
		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle("ChatGUI")
		self.setWindowIcon(QtGui.QIcon("icons\sina.png"))
		self.show()
		self.chatInput.setFocus()
	
	# exit - Exits the program.
	#
	def exit(self):
		sys.exit(0)

	# appendusers - Adds users to the user dictionary data structure
	#
	def appendusers(self, userName):
		self.userList.append(userName)

	# setUserList - Updates the current visible list of users
	#
	def setUserList(self, user):
		usersText = "Users:\n----------\n" + user
		if self.userList.toPlainText() != usersText:
			self.userList.setText(usersText)
	
	# addMessage - Appends a message to the end of the chat log	
	def addMessage(self, message):
		if message:
			try:
				self.chatDisplay.append(message)
			except:
				pass

	# connectMessageInput - Connects a callable to the 'send' button
	def connectMessageInput(self, callable):
		self.chatInput.returnPressed.connect(callable)
		self.sendButton.clicked.connect(callable)


def main():
	app = QtGui.QApplication(sys.argv)
	ex = ChatGUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
