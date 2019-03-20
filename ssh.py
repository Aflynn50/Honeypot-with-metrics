from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
class SSHpot():

    def run(self):
        with open('key.txt') as privateBlobFile:
            privateBlob = privateBlobFile.read()
            privateKey = Key.fromString(data=privateBlob)

        with open('key.txt.pub') as publicBlobFile:
            publicBlob = publicBlobFile.read()
            publicKey = Key.fromString(data=publicBlob)

        factory = SSHFactory()
        factory.privateKeys = {'ssh-rsa': privateKey}
        factory.publicKeys = {'ssh-rsa': publicKey}
        factory.portal = Portal(None)

        reactor.listenTCP(2222, factory)
