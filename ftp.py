from twisted.protocols.ftp import FTPFactory, FTPRealm, FTP
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.python import log
import sys

class FTPpot():
    def run(self):
        p = Portal(FTPRealm('./'), [])
        log.startLogging(sys.stdout)

        f = FTPFactory(p)

        reactor.listenTCP(2221, f)
