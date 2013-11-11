#!/usr/bin/python                                                                                                                             

from socket import *
import re
import thread
import sys

class ChatClient:

    userName = ""
    serverPort = 0

    # constructor                                                                                                                             
    def __init__(self, serverPort):
        self.serverPort = serverPort

    # handle_connection                                                                                                                       
    def send_username(self, serverPort):
        request = connectionSocket.recv(1024)
        regex = re.compile(request)

    def process_command(self,command):
        if not command:
            print "Error, username not provided. Program terminated"
            sys.exit()
        else:
            self.userName = command

    def send_message(self,message,serverSocket):
        message = "PUT " + message
        serverSocket.send(message)

    def send_get(self,serverSocket):
        while(1):
            message = "GET"

            serverSocket.send(message)

            try:

                for i in 1:2:
                    chats = serverSocket.recv(4196)
                    chatsArray = chats.split(" ",1)
                    if chatsArray[0] == "USERS":
                        print("David is gay")

                    elif chatsArray[0] == "MSGS":
                        print("David is really gay")

            except Exception, e:
                import traceback
    		print traceback.format.exc()
    
    def check_status(self,status):
        if status == "OK":
            print "ok to chat"

	else:
            print status

    def run(self):
	self.process_command(sys.argv[1])
        serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.settimeout(.25)
        serverSocket.connect(('localhost',self.serverPort))
	serverSocket.send("NAME " + self.userName)
        status = serverSocket.recv(256)
        self.check_status(status)
        self.send_message("Tim Jassman loves the D",serverSocket)
        status = serverSocket.recv(256)
        self.check_status(status)
	self.send_get(serverSocket)
        thread.start_new_thread(self.send_get,(serverSocket,))
        while(1):
            a = 0
            
client = ChatClient(15008)
client.run()


\

