# Project: create a load of low interation honeypots to find a new attack, leave up for a while and find bugs
import time
import socket
import threading
import requests
import matplotlib.pyplot as plt
import geopandas as gpd
import descartes

import http.server
import socketserver


from telnet import telnet
from vnc import vnc
from ftp import ftp

logfile = 'log.txt'
credfile = 'info/creds.txt'
lock = threading.Lock()
cv = threading.Condition()
stop = False
pots = []
listeners = []


class Pot(threading.Thread):
    def __init__(self, port, protocol_func):
        threading.Thread.__init__(self)
        self.port = port
        self.proto = protocol_func
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0', self.port))
        self.s.listen(100)

    def run(self):
        print('Starting ' + self.proto.__name__ + ' honeypot!')
        while True:
            (insock, address) = self.s.accept()
            if stop:
                cv.acquire()
                cv.notify_all()
                cv.release()
                print("Shutdown " + self.proto.__name__+' honeypot')
                return
            print('Connection from: {}:{} on port {}, the '.format(address[0], address[1], self.port) + self.proto.__name__+' honeypot')
            u, p = self.proto(insock, address)
            insock.close()
            lock.acquire()
            write_ip_log(str(address[0]))
            if u:
                write_cred_log(str(u), str(p))
            lock.release()
            cv.acquire()
            cv.notify_all()
            cv.release()


class BasicListner(threading.Thread):
    def __init__(self, port_num):
        self.working = True
        self.port = port_num
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('0.0.0.0', port_num))
            self.s.listen(1)
        except Exception:
            self.working = False

    def run(self):
        if not self.working:
            return
        while True:
            (insock, address) = self.s.accept()
            if stop:
                cv.acquire()
                cv.notify_all()
                cv.release()
                print("Shutdown listener on port " + self.port)
                return
            insock.close()
            lock.acquire()
            write_ip_log(str(address[0]))
            lock.release()
            cv.acquire()
            cv.notify_all()
            cv.release()


def write_ip_log(address):
    infile = False
    with open(logfile, 'r') as log:
        if address in map((lambda x: x.split(',')[0]), log.readlines()):
            infile = True
    if not infile:
        with open(logfile, 'a') as log:
            log.write(address + "\n")


def write_cred_log(user, password):
    with open(credfile, 'a') as cred:
        cred.write(user + ',' + password + "\n")


class Visualiser(threading.Thread):
    def __init__(self, logf):
        threading.Thread.__init__(self)
        self.places = []
        self.logfile = logf
        open(logf, 'w').close()
        self.api_key = "7424304154661ba7476d457c0adb3a1a"
        self.ip_getter = "http://api.ipstack.com/{0}?access_key={1}&fields=country_code"
        self.shapefile = "TM_WORLD_BORDERS-0.3.shp"
        self.gdf = gpd.read_file(self.shapefile)[['ISO2', 'geometry']].to_crs('+proj=robin')

    def update_data(self):
        with open(self.logfile, 'r') as log:
            lines = log.readlines()
            for i in range(len(lines)):
                info = lines[i].split(",")
                if len(info) == 1:
                    url = self.ip_getter.format(str(lines[i]), self.api_key)
                    ccode = str(requests.get(url).json()['country_code'])  # Fetch country code of IPs in file
                    lines[i] = lines[i][:-1] + "," + ccode + "\n"
                    self.places.append(ccode)
        with open(self.logfile,'w') as log:
            log.writelines(lines)

    def run(self):
        while True:
            if stop:
                plt.savefig("info/map.png")
                print("Visualiser shut down")
                return
            self.update_data()
            self.gdf['Count'] = self.gdf['ISO2'].map((lambda x: self.places.count(x)))
            print(self.places)
            ax = self.gdf.dropna().plot(column='Count', cmap='Reds', figsize=(16, 10), k=9)
            plt.show()
            cv.acquire()
            cv.wait()
            cv.release()

def httpServer():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 80), handler) as httpd:
        print("serving at port", 80)
        httpd.serve_forever()

def stopthread():
    global stop
    input("press enter to stop")
    print("stopping")
    stop = True
    for pot in pots:
        socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM).connect(('0.0.0.0', pot.port))
        pot.s.close()


def main():
    ports_and_headers = [(23, telnet), (21, ftp)] #(5900, vnc)

    for pair in ports_and_headers:
        pots.append(Pot(pair[0], pair[1]))
    v = Visualiser(logfile)

    for p in range(1,65535):
        listeners.append(BasicListner(p))
        listeners[:-1].start()

    for pot in pots:
        pot.start()



    v.start()
    threading.Thread(target=stopthread).start()
    threading.Thread(target=httpServer())


if __name__ == '__main__':
    main()
