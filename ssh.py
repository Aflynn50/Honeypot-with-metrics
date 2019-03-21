# https://stackoverflow.com/questions/36758571/python-ssh-servertwisted-conch-get-the-users-commands
import time
import socket


def writeLog(client, data=''):
    separator = '=' * 50
    fopen = open('./honey.mmh', 'a')
    fopen.write('Time: %s\nIP: %s\nPort: %d\nData: %s\n%s\n\n' % (time.ctime(), client[0], client[1], data, separator))
    fopen.close()


def main(host, port, motd):
    print('Starting honeypot!')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(100)
    while True:
        (insock, address) = s.accept()
        print('Connection from: %s:%d' % (address[0], address[1]))
        try:
            insock.send(motd.encode())
            data = insock.recv(1024)
            insock.close()
            print(data)
        except socket.error:
            print(address)
        else:
            print(address + "  " + data)


main("0.0.0.0", 2222, "hello there")


