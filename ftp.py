def ftp(insock, address):
    try:
        user = ""
        password = ""
        insock.sendall("220 (vsFTPd 3.0.3)\n".encode())
        command = str(insock.recv(1024))[2:-5]
        if command.startswith('USER'):
            user = command[5:]
        insock.sendall('331 Please specify the password.\n'.encode())
        command = str(insock.recv(1024))[2:-5]
        if command.startswith('PASS'):
            password = command[5:]
        insock.sendall('230 Login successful.\n'.encode())
        return user, password
    except Exception:
        return "", ""
