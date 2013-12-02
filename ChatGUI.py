"""
ChatGUI: class that client GUI




author: David Kale, Sina Tashakkori, Tim Jassman
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

	#  initUI - method that creates GUI components in the proper order, sets the desired
	#           measurements for those components, puts the components together, and then
	#	    	makes them visible to the user.
	#
	def initUI(self):
		# Displays the list of users
		self.userList = QtGui.QTextEdit("Users:", self)
		self.userList.setReadOnly(True)
		self.userList.setFixedWidth(100)

		# Displays the chat
		self.chatDisplay = QtGui.QTextEdit(self)
		self.chatDisplay.setReadOnly(True)
		#self.chatDisplay.verticalScrollBar().rangeChanged.connect(self.updateScrollBar)

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

		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle("ChatGUI")
		self.setWindowIcon(QtGui.QIcon("icons\sina.png"))
		self.show()
		self.chatInput.setFocus()
	
	# exit - method that exits the program.
	#
	def exit(self):
		sys.exit(0)

	# sendmessage - method that takes the users input from the GUI text field, then appends
	#               it to the bottom of the chat window to be displayed to current user. 
	#
	def sendmessage(self):
		message = self.chatInput.text()
		if message:
			self.chatInput.clear()
			self.chatDisplay.append(message)

	# getmessage - getter method, returns the text typed into the input text field.
	#
	def getmessage(self):
		message = self.chatInput.text()
		if message:
			self.chatInput.clear()
		return message

	# appendusers - method that adds users to the user dictionary data structure
	#
	def appendusers(self, userName):
		self.userList.append(userName)

	# setUserList - method that 
	#
	def setUserList(self, user):
		usersText = "Users:\n----------\n" + user
		if self.userList.toPlainText() != usersText:
			self.userList.setText(usersText)
	
	# updateUserList - method that
	#
	def updateUserList(self, signum, frame):
		print "ASD"
		self.userList.clear()

	
	def addMessage(self, message):
		if message:
			try:
				self.chatDisplay.append(message)
			except:
				pass

	def connectMessageInput(self, callable):
		self.chatInput.returnPressed.connect(callable)
		self.sendButton.clicked.connect(callable)

	def connectUserList(self, callable, text):
		self.userList.setText(text).connect(callable)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = ChatGUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
