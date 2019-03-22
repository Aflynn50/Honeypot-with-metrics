def ftp(insock, address):
    user = ""
    password = ""
    insock.sendall("220 (vsFTPd 3.0.3)\n")
    command = str(insock.recv(1024))
    if command.startswith('USER'):
        print(command[4:])
        user = command[4:]
    insock.sendall('331 Please specify the password.\n')
    command = str(insock.recv(1024))
    if command.startswith('PASS'):
        print(command[4:])
        password = command[4:]
    insock.sendall('230 Login successful.\n')
    return user, password
