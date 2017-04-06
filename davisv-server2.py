#
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
############################################################
# Rudimentary Messaging Server
# Created originally by Dr. Matt Jadud
# Modified extensively by Vincent Davis
# Implemented by Vincent Davis:
# Login Protocol
# Object Oriented Design
# 'REGISTER', 'MESSAGE', 'COUNT', 'DELMSG', 'GETMSG', 'DUMP', 'LOGIN', 'LOGOUT','CLOSE', etc. class methods
#
# Acknowledgement to Dr. Matt Jadud for original code, receive message functions and original main function
############################################################


import socket
import sys
import hashlib

#crypto library for RSA


class Server(object):

    # CONTRACT
    # start_server : string number -> socket
    # Takes a hostname and port number, and returns a socket
    # that is ready to listen for requests
    def __init__(self,host,port):
        self.MBX = {} #TODO: change these dictionaries to open a file and extract contents (maybe use SQLlite)
        self.IMQ = []
        self.LOGDICT = {}
        self.connection = None
        self.message=None
        self.result=None
        self.commanddict = {'REGISTER': self.register, 'MESSAGE': self.mmessage, 'COUNT': self.count,
                            'DELMSG': self.delmsg, 'GETMSG': self.getmsg, 'DUMP': self.dump,
                            'LOGIN': self.login, 'LOGOUT': self.logout, 'CLOSE': self.close_connection}
        ##################################################################################
        self.LOGIN = None
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)


    def __str__(self,x):
        return str(x)

    # CONTRACT
    # get_message : socket -> Tuple(string, socket)
    # Takes a socket and loops until it receives a complete message
    # from a client. Returns the string we were sent.
    # No error handling whatsoever.
    def get_message(self):
        # Acknowledgment: Received help from Quinten
        chars = []
        self.connection, client_address = self.sock.accept()
        try:
            while True:
                chunk = self.connection.recv(1)
                if chunk == b'':
                    raise RunTimeError("Connection Broken")
                    # break
                elif chunk == b'\0':
                    break
                else:
                    chars.append(chunk)
        finally:
            # print chars
            self.message = ''.join(chars)
            return self.message

    ##########################################################
    def register(self):
        meat = self.message.split(' ')[1:3]
        username = meat[0]
        password = meat[1]
        # username=message[9:]
        if username not in self.LOGDICT:
            self.MBX[username] = []
            self.LOGDICT[username] = password
            self.result = 'OK: User ' + username + ' registered. Password length: ' + str(len(password))
        else:
            self.result = 'KO: User already registered!'

    def mmessage(self):
        if self.LOGIN is not None:
            meat = self.message.split(' ')[1:]
            username = meat[0]
            print username
            length = len(username)
            mail = self.message[8 + length:]
            self.MBX[username].append(mail)
            self.result = 'OK: message sent to ' + username + '.'
        else:
            self.result = 'KO: No one is logged in.'

    def count(self):
        if self.LOGIN is not None:
            self.result = 'COUNTED ' + str(len(self.MBX[self.LOGIN]))
        else:
            self.result = 'KO: No one is logged in.'

    def delmsg(self):
        if self.LOGIN is not None:
            self.MBX[self.LOGIN].pop(0)
            self.result = 'OK: Oldest message deleted.'
        else:
            self.result = 'KO: No one is logged in.'

    def getmsg(self):
        if self.LOGIN is not None:
            self.result = self.MBX[self.LOGIN][0]
        else:
            self.result = 'KO: No one is logged in.'

    def dump(self):
        print self.MBX
        print self.IMQ
        print self.LOGDICT
        self.result = 'OK: Server dumped.'

    def login(self):
        meat = self.message.split(' ')[1:3]
        username = meat[0]
        password = meat[1]
        if username in self.LOGDICT:  # this can be shortened!
            if password == self.LOGDICT[username]:
                self.LOGIN = username
                self.result = 'OK: ' + username + ' logged in.'
            else:
                self.result = 'KO: password does not match file.'
        else:
            self.result = 'KO: No user by that name. Register?'

    def logout(self):
        self.LOGIN = None
        self.result = 'OK: User logged out.'

    def close_connection(self):
        self.LOGIN = None  # logout user
        # TODO: have function to save current states of dictionaries before closing the connection
        self. result = 'OK: Connection closed.'

    ###################################################################

    @property #what the hell is this?????????
    def handle_message(self):
        # "REGISTER" <username> <password> <checksum>-> add <username> to LOGDICT, value = <password>, add <username> to MBX, value [] return OK
        # "MESSAGE" [content] <checksum> -> interpret as message, add to MBX of user, return OK
        # "COUNT" <checksum> -> interpret rest as username, return "COUNTED <n>" or KO
        # "DELMSG" <checksum> -> interpret rest as username, delete 1st msg in MBX ,return OK or return KO
        # "GETMSG" <checksum> -> interpret rest as username, return 1st msg or return KO
        # "DUMP" <checksum> -> (server side) print contents of IMQ,MBX and return OK
        # "LOGIN" <username> <password> <checksum> -> checks for <username> in LOGDICT, is present, compares key to <password>
        # "LOGOUT" <checksum> -> set value of LOGIN to None
        # "CLOSE" <checksum> -> saves dictionaries, sets connection to close bidirectionally


        #TODONE! Implement a dictionary of functions
        #COMLST = ['REGISTER', 'MESSAGE', 'COUNT', 'DELMSG', 'GETMSG', 'DUMP', 'LOGIN', 'LOGOUT','CLOSE']
        command = self.message.split(' ')[0]
        checksum = self.message.split(' ').pop(-1)
        self.message = ' '.join(self.message.split(' ')[:-1])
        msgchecksum = self.calcsum(self.message)
        """
        print "Serverside checksum: " + checksum
        print "Clientside checksum: " + msgchecksum
        print "Message after slice: " + self.message
        raw_input("press enter")
        """
        if checksum != msgchecksum:
            return "KO: Checksum mismatch!"
        try:
            self.commanddict[command]()
        except KeyError:
            return 'KO: No handler for that command.'
            """
        if command in COMLST:  #TODO use try, except clause instead of COMLST
            self.commanddict[command]()


            if command == COMLST[0]:  # REGISTER
                meat = message.split(' ')[1:3]
                username = meat[0]
                password = meat[1]
                # username=message[9:]
                if username not in self.LOGDICT:
                    self.MBX[username] = []
                    self.LOGDICT[username] = password
                    return 'OK: User ' + username + ' registered. Password length: ' + str(len(password))
                else:
                    return 'KO: User already registered!'

            if command == COMLST[1]:  # MESSAGE
                if self.LOGIN != None:
                    meat = message.split(' ')[1:]
                    username = meat[0]
                    print username
                    length = len(username)
                    mail = message[8 + length:]
                    self.MBX[username].append(mail)
                    return 'OK: message sent to ' + username + '.'
                else:
                    return 'KO: No one is logged in.'

            if command == COMLST[2]:  # COUNT
                if self.LOGIN != None:
                    return 'COUNTED ' + str(len(MBX[LOGIN]))
                else:
                    return 'KO: No one is logged in.'


            if command == COMLST[3]:  # DELMSG
                if self.LOGIN != None:
                    self.MBX[self.LOGIN].pop(0)
                    return 'OK: Oldest message deleted.'
                else:
                    return 'KO: No one is logged in.'

            if command == COMLST[4]:  # GETMSG
                if self.LOGIN != None:
                    return self.MBX[self.LOGIN][0]
                else:
                    return 'KO: No one is logged in.'

            if command == COMLST[5]:  # DUMP
                print self.MBX
                print self.IMQ
                print self.LOGDICT
                return 'OK: Server dumped.'

            if command == COMLST[6]:  # LOGIN
                meat = message.split(' ')[1:3]
                username = meat[0]
                password = meat[1]
                if username in self.LOGDICT:  # this can be shortened!
                    if password == self.LOGDICT[username]:
                        self.LOGIN = username
                        return 'OK: ' + username + ' logged in.'
                    else:  # TODO: implement counting feature to block intruders
                        return 'KO: password does not match file.'
                else:
                    return 'KO: No user by that name. Register?'

            if command == COMLST[7]:  # LOGOUT
                self.LOGIN = None
                return 'OK: User logged out.'

            if command == COMLST[8]:
                self.LOGIN = None #logout user
                #TODO: have function to save current states of dictionaries before closing the connection
                return 'OK: Connection closed.'

        else:
            return 'KO: No handler for that command.'
            """

    ##########################################################


    # CONTRACT
    # socket -> boolean
    # Shuts down the socket we're listening on.
    def stop_server(self):
        return self.connection.close()


    # CONTRACT
    # handle_message : string socket -> boolean
    # Handles the message, and returns True if the server
    # should keep handling new messages, or False if the
    # server should shut down the connection and quit.
    def calcsum(self, msg):
        checksum = hashlib.md5(msg).hexdigest()
        return checksum





if __name__ == "__main__":
    # Check if the user provided all of the
    # arguments. The script name counts
    # as one of the elements, so we need at
    # least three, not fewer.
    if len(sys.argv) < 3:
        print ("Usage: ")
        print (" python server.py <host> <port>")
        print (" e.g. python server.py localhost 8888")
        print
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    server = Server(host, port)
    print("Running server on host [{0}] and port [{1}]".format(host, port))

    RUNNING = True
    while RUNNING:
        server.get_message()
        # print message
        print("MESSAGE: [{0}]".format(server.message))
        server.handle_message
        print "Result: {0}\nMessage: {1}\n".format(server.result, server.message)
        server.connection.sendall(bytes("{0}\0".format(server.result)))
        if server.result == 'KO: No handler for that command.':
            RUNNING = False
            #connection.close()
        elif server.result == 'OK: Connection closed.':
            RUNNING = False
            #print 'it closes if i have this print statement (not really)'
    server.stop_server()