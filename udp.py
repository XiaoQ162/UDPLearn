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

def client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = input('Input lowercase sentence: ')
    data = message.encode('ascii')
    s.sendto(data, ('127.0.0.1', port))
    print('THe OS assigned the address {} to me'.format(s.getsockname()))
    data, address = s.recvfrom(MAX_SIZE_BYTES)
    text = data.decode('ascii')
    print('The server {} replied with {!r}'.format(address, text))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000, help='UDP port (default 3000)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)