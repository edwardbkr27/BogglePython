import socket
import threading

############################
# Group A Skill 
# OOP: Classes
############################

class Host:
    ############################
    # Group A Skill 
    # Complex Client Server Model
    ############################
    
    def __init__(self):
        # Combines random port and local ip address to create a socket
        # A server is established using this socket
        self.port = 6791
        self.serverip = socket.gethostbyname(socket.gethostname())
        self.socket = (self.serverip, self.port)
        self.host = None
        self.hasConnected = True
        self.doServer = True
        self.msg = ""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.socket)
        self.endConnection = False

    # Run as a thread, allowing the server to listen in the background
    # Continually runs as a server
    def startServer(self):
        self.server.listen()
        while self.doServer == True:
            try:
                self.host = self.server.accept()[0]
            except OSError:
                pass
            if self.endConnection == True:
                self.hasConnected = False
                self.doServer = False
                break
            thread = threading.Thread(target=self.doConnection)
            thread.start()

    # Also run as a thread, listens for messages while connected
    # Listens to be sent the length of the incoming message, then recieves another message using this length only if a first message was recieved
    # If the hasConnected attribute is ever set to false, the server stops.
    def doConnection(self):
        while self.hasConnected == True:
            try:
                msg_length = self.host.recv((2^7)).decode("utf-8")
            except ConnectionResetError:
                quit()
            if msg_length:
                msg_length = int(msg_length)
                self.msg = self.host.recv(msg_length).decode("utf-8")
            if self.endConnection == True:
                self.hasConnected = False
                self.doServer = False
                break
        self.host.shutdown(socket.SHUT_RDWR)
        self.host.close()
        self.server.close()

    # Broadcasts a message for the client to recieve
    def broadcastMessage(self, msg):
        if not self.endConnection:
            self.host.send(str(msg).encode("utf-8"))

    # Matches a message from the client to a string
    def getMsg(self, match):
        if self.msg.upper() == match.upper():
            return True
        else:
            return False

    # Sets the hasConnected attribute to false
    # is called from other classes when the online game ends
    def doExit(self):
        self.hasConnected = False