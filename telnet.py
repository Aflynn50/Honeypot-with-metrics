def telnet(insock, address):
    insock.send("Welcome to my fake Telnet server\n\nlogin: ".encode())
    user = insock.recv(1024)
    insock.send("password: ".encode())
    password = insock.recv(1024)
    return user, password
