# Messaging Client
############################################################
# Rudimentary Messaging Client
# Created originally by Dr. Matt Jadud
# Modified extensively by Vincent Davis
#
#
# Acknowledgement to Dr. Matt Jadud for original code
############################################################





import socket
import sys
import hashlib

MSGLEN = 1


# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
class Client(object):
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.sock = None
        # self.testconnect()


    def testconnect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))
            #self.sock.close()
            print 'Connection successful!'
            return True
        except socket.error:
            print "a problem occurred when trying to connect"
            return False


    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def calcsum(self, msg):
        checksum = hashlib.md5(msg).hexdigest()
        return checksum

    def receive_message(self, sock):
        chars = []
        try:
            while True:
                char = self.sock.recv(1)
                if char == b'\0':
                    break
                if char == b'':
                    break
                else:
                    # print("Appending {0}".format(char))
                    chars.append(char.decode("utf-8"))
        finally:
            return ''.join(chars)

    def send(self, msg):
        ch = "CHECKSUM "
        self.connect()
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect((HOST, PORT))
        length = self.sock.send(bytes(msg+ " " + self.calcsum(msg)) + "\0")
        #checksum = sock.send(ch+calcsum(msg) + "\0")
        print ("SENT MSG: '{0}'".format(msg))
        # print ("SENT CHECKSUM: '{0}'".format(checksum))
        print ("CHARACTERS SENT: [{0}]".format(length))
        # return self.sock

    def recv(self):
        response = self.receive_message(self.sock)
        print("RESPONSE: [{0}]".format(response))
        self.sock.close()
        return response

    def send_recv(self, msg):
        while True:
            self.send(msg)
            response = self.recv()
            if response == "KO: Checksum mismatch!":
                continue
            else:
                break


if __name__ == "__main__":
    # Check if the user provided all of the
    # arguments. The script name counts
    # as one of the elements, so we need at
    # least three, not fewer.
    if len(sys.argv) < 3:
        print ("Usage:")
        print (" python client.py <host> <port>")
        print (" For example:")
        print (" python client.py localhost 8888")
        print
        sys.exit()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    clientobj = Client(HOST, PORT)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((HOST, PORT))
    stay_connected = clientobj.testconnect()
    try:
        while stay_connected:  # TODO: Add more capabilities. take in input as a psuedo terminal
            #TODO: Enumeration?
            input = raw_input('What would you like to do?')
            print '(1): Test function.','(2): End connection (both sides).'
            if input == '1':
                clientobj.send_recv("DUMP")
                clientobj.send_recv("REGISTER jadudm password123")
                clientobj.send_recv("REGISTER jadudm password123")
                clientobj.send_recv('LOGIN jadudm password123')
                clientobj.send_recv("MESSAGE jadudm Four score and seven years ago.")
                clientobj.send_recv("DUMP")
                clientobj.send_recv("GETMSG")
                clientobj.send_recv("DELMSG")
                clientobj.send_recv("LOGOUT")
                clientobj.send_recv("MESSAGE jadudm Four score and seven years ago.")
                clientobj.send_recv("DUMP")
            elif input == '2':
                clientobj.send_recv("CLOSE")
                stay_connected = False
    except socket.error:
        print "a problem occurred along the way (probably refused connection)"
