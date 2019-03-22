def telnet(insock, address):
    insock.send("Welcome to my fake Telnet server\n\nlogin: ".encode())
    user = str(insock.recv(1024))
    insock.send("password: ".encode())
    password = str(insock.recv(1024))
    insock.send("".encode())
    return user, password
