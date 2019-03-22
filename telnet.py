def telnet(insock, address):
    insock.send("Welcome to my fake Telnet server\n\nlogin: ".encode())
    user = insock.recv(1024)[2:].strip()
    insock.send("password: ".encode())
    password = insock.recv(1024)[2:].strip()
    insock.send("".encode())
    return user, password
