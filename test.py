import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.0.101',8000)
message = 'This is the message.  It will be repeated.'
try:
    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()


