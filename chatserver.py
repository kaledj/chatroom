#!/usr/bin/python                                                                                                                                                                 

from socket import *
import re
import thread
import select

class ChatServer:
    serverPort = 0
    backlog = 5
    clientSockets = []
    clientInfo = []
    # constructor                                                                                                                                                                 
    def __init__(self, serverPort):
        self.serverPort = serverPort

    # run                                                                                                                                                                         
    def run(self):
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',self.serverPort))
        serverSocket.listen(self.backlog)
        inputs = [serverSocket]
        print ("Server ready for chat clients")
        while(1):
            inputready, outputready, exceptready = select.select(inputs, [], [])
            for s in inputready:
                if s == serverSocket:
                    connectionSocket, addr  = serverSocket.accept()
                    inputs.append(connectionSocket)
                    self.clientSockets.append(connectionSocket)
                elif s in self.clientSockets:
                    thread.start_new_thread(self.handle_connection,(s,))

    # handle_connection                                                                                                                                                           
    def handle_connection(self, connectionSocket):
        request = connectionSocket.recv(1024)
        splitRequest = re.split('[\r\n ]+', request);
        if splitRequest[0] == "NAME":
            if len(splitRequest) == 2:
                self.clientInfo.append([connectionSocket,splitRequest[1],[]])
                print splitRequest[1]
                connectionSocket.send("OK")
        elif splitRequest[0] == "GET":
            a=5  
        elif splitRequest[0] == "PUT":
            a=5
        elif splitRequest[0] == "USERS":
            data = "MSGS Users:"
            for i in self.clientInfo:
                data += "\n"+i[1]
            print data
            connectionSocket.send(data)


server = ChatServer(15008)
server.run()
