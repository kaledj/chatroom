#!/usr/bin/python                                                                                                                                                                 

from socket import *
import re
import thread

clientSockets = []
serverPort = 0

class ChatServer:

    # constructor                                                                                                                                                                 
    def __init__(self, serverPort):
        self.serverPort = serverPort

    # run                                                                                                                                                                         
    def run(self):
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',self.serverPort))
        serverSocket.listen(5)
        print ("Server ready for chat clients")
        while(1):
            connectionSocket, addr  = serverSocket.accept()
            clientSockets.append(connectionSocket)
            thread.start_new_thread(self.handle_connection,(connectionSocket,))

    # handle_connection                                                                                                                                                           
    def handle_connection(self, connectionSocket):
        request = connectionSocket.recv(1024)
        regex = re.compile(request)


server = ChatServer(15005)
server.run()
