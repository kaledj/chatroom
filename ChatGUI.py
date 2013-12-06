#!/usr/bin/python

"""
ChatGUI.py: Defines a python class that implements a GUI for the chatroom. 
			Utilizes PyQt4 for GUI components.

author: David Kale, Sina Tashakkori, Tim Jassmann
version: 2
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
		# Create dialogs
		self.createDialogs()

		# Create a menuBar
		self.initMenuBar()

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

		# Button to attach a file
		self.attachFileButton = QtGui.QPushButton(self)
		self.attachFileButton.setIcon(QtGui.QIcon("icons\clip.png"))
		self.attachFileButton.setToolTip("Attach a file")
		
		# Layout management
		#self.menuBarBox = QtGui.QHBoxLayout()
		self.displayBox = QtGui.QHBoxLayout()
		self.displayBox.addWidget(self.chatDisplay)
		self.displayBox.addWidget(self.userList)
		self.sendBox = QtGui.QHBoxLayout()
		self.sendBox.addWidget(self.chatInput)
		self.sendBox.addWidget(self.attachFileButton)
		self.sendBox.addWidget(self.sendButton)
		self.container = QtGui.QVBoxLayout(self)
		self.container.setMenuBar(self.menuBar)
		self.container.addLayout(self.displayBox)
		self.container.addLayout(self.sendBox)
		self.statusBar = QtGui.QStatusBar(self)
		self.statusBar.setFixedHeight(15)
		self.statusBar.showMessage("Language: " + self.prefsDialog.langSelect.currentText())
		self.statusBarLayout = QtGui.QVBoxLayout()
		self.statusBarLayout.addWidget(self.statusBar)
		self.container.addLayout(self.statusBarLayout)
		self.setLayout(self.container)

		# Display the window
		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle("ChatGUI")
		self.setWindowIcon(QtGui.QIcon("icons\sina.png"))
		self.show()
		self.chatInput.setFocus()

	def initMenuBar(self):
		self.menuBar = QtGui.QMenuBar()
		self.initFileMenu()
		self.initEditMenu()
		self.initHelpMenu()

	def createDialogs(self):
		# Login dialog
		self.loginDialog = QtGui.QInputDialog(self)
		# Preferences
		self.prefsDialog = QtGui.QDialog(self)
		self.prefsDialog.setWindowTitle("Preferences")
		self.prefsDialog.prefsContainer = QtGui.QHBoxLayout(self.prefsDialog)
		self.prefsDialog.langLabel = QtGui.QLabel("Language:")
		self.prefsDialog.langSelect = QtGui.QComboBox()
		self.prefsDialog.langSelect.addItems(["en", "es", "pt", "de", "fr", "it", "nl"])
		self.prefsDialog.langSelect.currentIndexChanged.connect(self.changeLanguage)
		self.prefsDialog.prefsContainer.addWidget(self.prefsDialog.langLabel)
		self.prefsDialog.prefsContainer.addWidget(self.prefsDialog.langSelect)
		self.prefsDialog.setLayout(self.prefsDialog.prefsContainer)

	def initFileMenu(self):
		# Create exit action
		exitAction = QtGui.QAction(QtGui.QIcon('icons\sina.png'), '&Exit', self)
		exitAction.triggered.connect(QtGui.qApp.quit)
		# Create file menu and add actions
		fileMenu = self.menuBar.addMenu('&File')
		fileMenu.addAction(exitAction)

	def initEditMenu(self):
		# Create preferences action
		prefsAction = QtGui.QAction(QtGui.QIcon('icons\sina.png'), '&Preferences', self)
		prefsAction.triggered.connect(self.showPrefsDialog)
		# Create name change action
		changeUsernameAction = QtGui.QAction(QtGui.QIcon('icons\sina.png'), '&Change Username', self)
		changeUsernameAction.triggered.connect(self.changeUsernameDialog)
		# Create edit menu and add actions
		editMenu = self.menuBar.addMenu('&Edit')
		editMenu.addAction(prefsAction)
		editMenu.addAction(changeUsernameAction)

	def initHelpMenu(self):
		aboutAction = QtGui.QAction(QtGui.QIcon('icons\sina.png'), '&About', self)
		aboutAction.setStatusTip('About this software')
		aboutAction.triggered.connect(self.showAboutDialog)
		helpMenu = self.menuBar.addMenu('&Help')
		helpMenu.addAction(aboutAction)

	def showLoginDialog(self):
		input, status = self.loginDialog.getText(self, 'Chatroom Login', 
			'Username:')
		if status and input:
			self.emit(QtCore.SIGNAL("usernameGiven"), input)
		else:
			self.showLoginDialog()

	def showAboutDialog(self):
		self.aboutDialog = QtGui.QDialog(self)
		readme = open('README', 'r')
		aboutText = readme.read()
		about = QtGui.QTextEdit(self.aboutDialog)
		about.setFixedWidth(600)
		about.setText(aboutText)
		self.aboutDialog.setWindowTitle("About")
		self.aboutDialog.container = QtGui.QHBoxLayout(self.aboutDialog)
		self.aboutDialog.container.addWidget(about)
		self.aboutDialog.show()

	def changeUsernameDialog(self):
		input, status = self.loginDialog.getText(self, 'Change Username', 
			'Username:')
		if status and input:
			self.emit(QtCore.SIGNAL("usernameChanged"), input)

	def changeLanguage(self):
		self.statusBar.showMessage("Language: " + self.prefsDialog.langSelect.currentText())
		self.emit(QtCore.SIGNAL("languageChanged"), 
			self.prefsDialog.langSelect.currentText().toAscii())

	def showPrefsDialog(self):
		self.prefsDialog.show()

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
