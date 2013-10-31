#!/usr/bin/python      

from socket import *
import re
import thread
import sys

class ChatClient:

    userName = ""
    serverPort = 0
    users = []

    # constructor
    def __init__(self, serverPort):
        self.serverPort = serverPort

    # run 
    #def run(self):
    #    for arg in sys.argv:
    #        process_command(arg)

    #    return    
        #serverSocket = socket(AF_INET,SOCK_STREAM)
        #serverSocket.bind(('',self.serverPort))
        #serverSocket.listen(5)
        #print ("Server ready for chat clients")
        #while(1):
        #    connectionSocket, addr  = serverSocket.accept()
        #    clientSockets.append(connectionSocket)
        #    thread.start_new_thread(self.handle_connection,(connectionSocket,))
     
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
        return
            
    def run(self):
        self.process_command(sys.argv[1])
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.connect(('localhost',self.serverPort))
        serverSocket.send("NAME " + self.userName)
        status = serverSocket.recv(256)           
        if status == "OK":
            print "ok to chat"
            
        else:
            print status

        serverSocket.send("USERS")
        users = serverSocket.recv(4196)
        
        print status
    
        return

client = ChatClient(15008)
client.run()
