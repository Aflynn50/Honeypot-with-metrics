# https://stackoverflow.com/questions/36758571/python-ssh-servertwisted-conch-get-the-users-commands
from twisted.python import log
from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from twisted.internet import reactor
import sys
class SSHpot():

    def run(self):
        with open('ssh_key') as privateBlobFile:
            privateBlob = privateBlobFile.read()
            privateKey = Key.fromString(data=privateBlob)

        with open('ssh_key.pub') as publicBlobFile:
            publicBlob = publicBlobFile.read()
            publicKey = Key.fromString(data=publicBlob)

        factory = SSHFactory()
        factory.privateKeys = {'ssh-rsa': privateKey}
        factory.publicKeys = {'ssh-rsa': publicKey}
        factory.portal = Portal(None)
        log.startLogging(sys.stdout)
        reactor.listenTCP(2222, factory)
