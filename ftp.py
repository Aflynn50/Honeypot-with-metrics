def ftp(insock, address):
    user = ""
    password = ""
    insock.sendall("220 (vsFTPd 3.0.3)\n".encode())
    command = str(insock.recv(1024))
    print(command)
    if command.startswith('USER'):

        user = command
    insock.sendall('331 Please specify the password.\n'.encode())
    command = str(insock.recv(1024))
    print(command)
    if command.startswith('PASS'):

        password = command
    insock.sendall('230 Login successful.\n'.encode())
    return user, password
