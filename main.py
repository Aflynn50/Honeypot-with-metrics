# Project: create a load of low interation honeypots to find a new attack, leave up for a while and find bugs

from twisted.internet import reactor
from twisted.logger import Logger
from ssh import SSHpot
from ftp import FTPpot
from zope.interface import provider
from twisted.logger import ILogObserver, formatEvent


@provider(ILogObserver)
def simpleObserver(event):
    print(formatEvent(event))

s = SSHpot()
s.run()
#f = FTPpot()
reactor.run()
