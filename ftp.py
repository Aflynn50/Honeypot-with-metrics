def ftp(insock, address):
    user = ""
    password = ""
    insock.sendall("220 (vsFTPd 3.0.3)\n".encode())
    command = str(insock.recv(1024))
    if command.startswith('USER'):
        print(command[4:])
        user = command[4:]
    insock.sendall('331 Please specify the password.\n'.encode())
    command = str(insock.recv(1024))
    if command.startswith('PASS'):
        print(command[4:])
        password = command[4:]
    insock.sendall('230 Login successful.\n'.encode())
    return user, password
