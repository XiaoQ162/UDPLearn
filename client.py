import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = input('Input lowercase sentence: ')
data = message.encode('ascii')
s.sendto(data, ('127.0.0.1', 3000))
print('THe OS assigned the address {} to me'.format(s.getsockname()))
data, address = s.recvfrom(65535)
text = data.decode('ascii')
print('The server {} replied with {!r}'.format(address, text))