# Messaging Client
import socket
import sys

MSGLEN = 1

# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
"""
def receive_message (sock):
  #return "HELO"
  
  #Acknowledgment: Received help from Quinten
  
  message=""
  receiving = True
  while receiving == True:
    connection,client_address=sock.accept()
    chunk = connection.recv(8)
    if chunk == "":
      raise RunTimeError("Connection Broken")
    else:
      chunkcheck=list(chunk)
      for char in chunkcheck:
        if char == "\0":
          receiving=False
          break
        else:
          message+=char
  return message, connection
"""
def receive_message (sock):
  chars = []
  try:
    while True:
      char = sock.recv(1)
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return ''.join(chars)

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

  host = sys.argv[1]
  port = int(sys.argv[2])
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((sys.argv[1], int(sys.argv[2])))
  chars_sent = sock.send(b"MESSAGE <<<<<<<<<<<<>>>>>>>>>>>>\0")
  print ("CHARACTERS SENT: [{0}]".format(chars_sent))

  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))

  sock.close()
