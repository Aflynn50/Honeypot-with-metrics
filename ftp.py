from twisted.protocols.ftp import FTPFactory, FTPRealm, FTP
from twisted.cred.portal import Portal
from twisted.internet import reactor

class FTPpot():
    def run(self):
        p = Portal(FTPRealm('./'),None)

        f = FTPFactory(p)

        reactor.listenTCP(21, f)
