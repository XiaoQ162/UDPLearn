import argparse, socket

MAX_SIZE_BYTES = 65535 # Maximum size of a UDP datagram

def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Listening at {}'.format(s.getsockname()))
    while True:
        data, clientAddress = s.recvfrom(MAX_SIZE_BYTES)
        message = data.decode('ascii')
        upperCaseMessage = message.upper()
        print('The client at {} says {!r}'.format(clientAddress, message))
        data = upperCaseMessage.encode('ascii')
        s.sendto(data, clientAddress)

# The client function is almost identical to the one in client.py, 
# except that it uses the port number specified by the user instead of the hard-coded port number 3000.
# The client use sendto() to send the message to the server,
def clientSendTo(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = input('Input lowercase sentence: ')
    data = message.encode('ascii')
    s.sendto(data, ('127.0.0.1', port))
    print('THe OS assigned the address {} to me'.format(s.getsockname()))
    data, address = s.recvfrom(MAX_SIZE_BYTES)
    text = data.decode('ascii')
    print('The server {} replied with {!r}'.format(address, text))

# The client use connect() to connect to the server,
# Advantage: The client can use send() and recv() instead of sendto() and recvfrom().
# Disadvantage: The client can only communicate with the server.
def clientConnect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.connect((hostname, port))
    print('Client socket name is {}'.format(s.getsockname()))
    message = input('Input lowercase sentence: ')
    data = message.encode('ascii')
    s.send(data)
    print('THe OS assigned the address {} to me'.format(s.getsockname()))
    data = s.recv(MAX_SIZE_BYTES)
    text = data.decode('ascii')
    print('The server {} replied with {!r}'.format(s.getpeername(), text))

def client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hosts = []
    while True:
        host = input('Input host: ')
        if host == '':
            break
        hosts.append(host)
        message = input('Input lowercase sentence: ')
        data = message.encode('ascii')
        s.sendto(data, (host, port))
        print('THe OS assigned the address {} to me'.format(s.getsockname()))
        data, address = s.recvfrom(MAX_SIZE_BYTES)
        text = data.decode('ascii')
        if (address[0] in hosts):
            print('The server {} replied with {!r}'.format(address, text))
            hosts.remove(address[0])
        else:
            print('message {!r} from {} is not in hosts'.format(text, address))

def chatServer(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Listening at {}'.format(s.getsockname()))
    clientAddresses = []
    while True:
        data, clientAddress = s.recvfrom(MAX_SIZE_BYTES)
        if (len(clientAddresses) == 0):
            clientAddresses.append(clientAddress)
        if (clientAddress not in clientAddresses):
            print('Received other client message from {}'.format(clientAddress))
        message = data.decode('ascii')
        print('The client at {} says {!r}'.format(clientAddress, message))
        reply = input('Input reply: ')
        data = reply.encode('ascii')
        s.sendto(data, clientAddress)

def chatClient(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.connect((hostname, port))
    print('Client socket name is {}'.format(s.getsockname()))
    while True:
        message = input('Input message: ')
        data = message.encode('ascii')
        s.send(data)
        print('THe OS assigned the address {} to me'.format(s.getsockname()))
        data = s.recv(MAX_SIZE_BYTES)
        text = data.decode('ascii')
        print('The server {} replied with {!r}'.format(s.getpeername(), text))


if __name__ == '__main__':
    choices = {'client': chatClient, 'server': chatServer}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000, help='UDP port (default 3000)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)