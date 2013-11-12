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

    def nameExists(self, name):
        for s in self.clientInfo:
            if s[1] == name:
                return True
        return False

    def getSocketInfo(self, connectionSocket):
        for s in self.clientInfo:
            if s[0] == connectionSocket:
                return s

    def socketInfoExists(self, connectionSocket):
        for s in self.clientInfo:
            if s[0] == connectionSocket:
                return True
        return False

    # handle_connection                                                                                                                                                           
    def handle_connection(self, connectionSocket):
        request = connectionSocket.recv(1024)
        splitRequest = request.split(' ', 1)
        if splitRequest[0] == "NAME":
            print request
            if len(splitRequest) == 2:
                if(self.nameExists(splitRequest[1])):
                    connectionSocket.send("ERROR Name is in use")
                    self.clientSockets.remove(connectionSocket)
                    connectionSocket.close()
                else:
                    self.clientInfo.append([connectionSocket,splitRequest[1],""])
                    self.clientSockets.remove(connectionSocket)
                    connectionSocket.send("OK")
            else:
                connectionSocket.send("ERROR Invalid name")
        elif splitRequest[0] == "GET":
            print request
            info = self.getSocketInfo(connectionSocket)
            connectionSocket.send("MSGS "+info[2])
            data = "USERS"
            for i in self.clientInfo:
                data += " "+i[1]
            connectionSocket.send(data);
            info[2] = ""
        elif splitRequest[0] == "PUT":
            print request
            try:
                if len(splitRequest) == 2:
                    name = self.getSocketInfo(connectionSocket)[1]
                    for s in self.clientInfo:
                        s[2] += "\n<"+name+">"+splitRequest[1]
                    connectionSocket.send("OK")
            except Exception:
                pass
        elif splitRequest[0] == "USERS":
            print request
            data = "MSGS \nUsers:"
            for i in self.clientInfo:
                data += "\n"+i[1]
            connectionSocket.send(data)

server = ChatServer(15008)
server.run()
