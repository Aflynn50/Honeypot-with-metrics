import binascii


def vnc(insock, address):
    insock.send(binascii.unhexlify("524642203030332e3030380a"))
    prot_ver = insock.recv(1024)
    insock.send(binascii.unhexlify('0102'))
    data = insock.recv(1024)
    print(data)
    insock.send(binascii.unhexlify('00000000'))
    data = insock.recv(1024)
    print(data)
    insock.send(binascii.unhexlify('043a02ff2018000100ff00ff00ff1008000000000000000d4745525449452d445747445747'))
    data = insock.recv(1024)
    print(data)
    return "username", "password"
