#
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys


# CONTRACT
# start_server : string number -> socket
# Takes a hostname and port number, and returns a socket
# that is ready to listen for requests
def start_server (host, port):
  server_address = (host, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(server_address)
  sock.listen(1)
  return sock
  
# CONTRACT
# get_message : socket -> Tuple(string, socket)
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def get_message (sock):
  #Acknowledgment: Received help from Quinten
  chars=[]
  connection,client_address=sock.accept()
  try:
     while True:
        chunk = connection.recv(1)
        if chunk == b'':
          raise RunTimeError("Connection Broken")
          #break
	    elif chunk == b'/0':
          break
        else:
          chars+=char
  finally:
    return (''.join(chars), connection)


##########################################################

MBX = {}
IMQ = []
def handle_message(message):
#"REGISTER <username>" -> interpret as username, add to MBX, value = [] return OK
#"MESSAGE <content>" -> interpret as message, add to IMQ, return OK
#"STORE <username>" -> interpret rest as username, pop most recent message off IMQ, append to username msg list return OK
#"COUNT <username>" -> interpret rest as username, return "COUNTED <n>" or KO
#"DELMSG <username>" -> interpret rest as username, delete 1st msg in MBX ,return OK or return KO
#"GETMSG <username>" -> interpret rest as username, return 1st msg or return KO
#"DUMP" -> (server side) print contents of IMQ,MBX and return OK
  COMLST=['REGISTER','MESSAGE','STORE','COUNT','DELMSG','GETMSG','DUMP']
  command = message.split(' ')[0]

  if command in COMLST:  #can you make a dictionary of functions??

    if command == COMLST[0]: #REGISTER
      username=message[9:]
      MBX[username]=[]
	  return 'OK: User '+ username + ' registered.'

    elif command == COMLST[1]: #MESSAGE
      mail= message[8:]
      IMQ.append(mail)
      return 'OK: message sent.'

    elif command == COMLST[2]: #STORE
      try:
        username = message[6:]
        MBX[username].append(IMQ.pop())
        return 'OK: Message stored to '+username+' inbox.'
      except KeyError:
        return 'KO: No user by that name.'

    elif command == COMLST[3]: #COUNT
      try:
        username = message[6:]
        return 'COUNTED '+ str(len(MBX[username]))
      except KeyError:
        return 'KO : No user by that name.'

    elif command == COMLST[4]: #DELMSG
      try:
        username = message[7:]
        IMQ = IMQ.pop(0)
        return 'OK: Oldest message deleted.'
      except KeyError:
        return 'KO: No user by that name.'

    elif command == COMLST[5]: #GETMSG
      try:
        username = message[7:]
        email = IMQ[0]
        return email
      except KeyError:
        return 'KO: No user by that name.'

    elif command == COMLST[6]: #DUMP
      print MBX
      print IMQ
      return 'OK: Server dumped.'

  else:
    return 'KO: No handler for that command.' #how to send back to client??

  

##########################################################
  
  

# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# CONTRACT
# handle_message : string socket -> boolean
# Handles the message, and returns True if the server
# should keep handling new messages, or False if the 
# server should shut down the connection and quit.
def handle_message (msg, conn):
  return False
  
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
  sock = start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  while RUNNING:
    message, connection = get_message(sock)
    print("MESSAGE: [{0}]".format(message))
    result = handle_message(message)
	print ("Result: {0}\nMessage: {1}\n".format(result))
    connection.sendall(bytes("{0}\0".format(result)))
	if result == 'KO: No handler for that command.':
      RUNNING = False
    connection.close()
  stop_server(sock)