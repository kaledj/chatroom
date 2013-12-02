#!/usr/bin/python                                                                                                                             

"""
chatclient.py: Defines a python class that implements a client for a chatroom. 

author: David Kale, Sina Tashakkori, Tim Jassmann
version: 1
"""

from ChatGUI import *
from socket import *
import re, thread, sys, signal, os
import time

class ChatClient(QtCore.QObject):

	userName = ""
	
	# Constructor                                                                                                                             
	#
	def __init__(self, serverPort):
		self.app = QtGui.QApplication(sys.argv)
		super(ChatClient, self).__init__()
		self.serverPort = serverPort
		self.GUI = ChatGUI()
		self.GUI.connectMessageInput(self.send_message)
		self.clientThread = thread.start_new_thread(self.run, ())
		# Connects relevant signals to GUI slots
		self.connect(self, QtCore.SIGNAL("updateUsers"), self.GUI.setUserList)
		self.connect(self, QtCore.SIGNAL("addMessage"), self.GUI.addMessage)
		self.connect(self, QtCore.SIGNAL("exit"), self.GUI.exit)
		self.app.exec_()

	# process_command - Takes expected command line arguments to initialize username.
	#
	def process_command(self,command):
		if not command:
			print "Error, username not provided. Program terminated"
			sys.exit()
		else:
			self.userName = command

	# send_message - Obtains the text from chat input and sends them to server. 
	#				 PUT is prepended to indicate the method.
	#
	def send_message(self):
		message = self.GUI.chatInput.text().toAscii()
		if message:
			message = "PUT " + message
			self.GUI.chatInput.clear()
			self.serverSocket.send(message)
		self.GUI.chatInput.setFocus()		

	# get_data - Polls the server for the most recent users list and the most
	#			 recent chat log. The specific functionality of each is delegated
	#			 to an appropriate function call.
	#
	def get_data(self):
		while(1):
			time.sleep(.25)
			self.get_users()
			self.get_msgs()

	# get_users - Polls the server for the most recent list of users. This
	#			  list is sent to the GUI.
	#
	def get_users(self):
		message = "GETUSERS"
		try:
			self.serverSocket.send(message)
			chats = self.serverSocket.recv(4196)
			chatsArray = chats.split(" ",1)
			if chatsArray[0] == "USERS":
				self.emit(QtCore.SIGNAL("updateUsers"), chatsArray[1])
		except Exception, e:
			print "Error connecting to server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)

	# get_msgs - Polls the server for the most recent chat log. When complete, 
	#            the GUI is notified via signal. 
	#
	def get_msgs(self):
		message = "GETMSGS"
		try:
			self.serverSocket.send(message)
			chats = self.serverSocket.recv(4196)
			chatsArray = chats.split(" ",1)
			if chatsArray[0] == "MSGS":
				self.emit(QtCore.SIGNAL("addMessage"), chatsArray[1])
			else:
				print "error in get_msgs"
		except Exception, e:
			print "Error connecting to server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)

	# check_status - Small helper method that checks a given server status.
	#		
	def check_status(self,status):
		if status == "OK":
			print "ok to chat"
		else:
			print status
			self.app.closeAllWindows()

	# run - Processes the command line arguments and checks for validity. Then, 
	#		establishes a TCP connection with the chatroom server. Main event
	#		based execution loop is entered, where a message may have been typed
	#		and sent by the GUI, and meanwhile the client simply polls the 
	#		server periodically for the most recent chat data. 
	#
	def run(self):
		try:
			self.process_command(sys.argv[1])
		except IndexError:
			print "Error: Must provide a username"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		self.serverSocket.settimeout(.25)
		try:
			self.serverSocket.connect(('student.cs.appstate.edu',self.serverPort))
			self.serverSocket.send("NAME " + self.userName)
			status = self.serverSocket.recv(256)
			self.check_status(status)
		except:
			print "Error contacting server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)
		self.get_data()
		while(1):
			a = 0

def main():
	client = ChatClient(15008)

if __name__ == '__main__':
	main()
