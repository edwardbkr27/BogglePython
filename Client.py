import socket

############################
# Group A Skill 
# OOP: Classes
############################

class Client:
    EMPTY = b' '
    ############################
    # Group A Skill 
    # Complex Client Server Model
    ############################

    def __init__(self):
        # Uses same port as server and gathers local ip to create socket
        # Client then connects to that socket
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6791
        self.serverip = socket.gethostbyname(socket.gethostname())
        self.socket = (self.serverip, self.port)
        self.user.connect(self.socket)
        self.endConnection = False
        self.mostRecentMsg = ""

    # Receives the message to be sent as a paramater
    # Message is encoded in utf8
    # The message needs to meet a length of 2^7 before it can be sent
    # The length of the message to be sent is determined
    # A string of empty spaces is created of length (2^7) - length of the message already
    # The empty spaces and message are then combined and sent
    # Additionally, the most recent message from the server is determined
    def send(self, msg):
        message = msg.encode("utf-8")
        len_msg = len(str(message))
        spaces = str(len_msg).encode("utf-8")
        spaces += self.EMPTY * ((2^7) - len(spaces))
        self.user.send(spaces + message)
        self.mostRecentMsg = self.getMsg()

    def doExit(self):
        self.user.close()

    # Gets a message from the host and decodes it
    def getMsg(self):
        try:
            return (self.user.recv(2048).decode("utf-8"))
        except:
            pass