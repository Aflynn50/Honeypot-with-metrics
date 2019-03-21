# Project: create a load of low interation honeypots to find a new attack, leave up for a while and find bugs
import time
import socket
import threading
import requests
import matplotlib.pyplot as plt
# import pandas as pd
# import pycountry as pyc
import geopandas as gpd
# import descartes


logfile = 'log.txt'

lock = threading.Lock()

cv = threading.Condition()

class Pot(threading.Thread):
    def __init__(self, port, header):
        threading.Thread.__init__(self)
        self.port = port
        self.header = header

    def run(self):
        print('Starting honeypot!')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.port))
        s.listen(100)

        while True:
            (insock, address) = s.accept()
            print('Connection from: {}:{} on port {}'.format(address[0], address[1], self.port))
            insock.send(self.header.encode())
            data = insock.recv(1024)
            insock.close()
            print(data)
            lock.acquire()
            write_log(str(address[0]))
            lock.release()
            cv.acquire()
            cv.notify_all()
            cv.release()


def write_log(client, data=''):
    with open(logfile, 'a') as log:
        log.write(client + "\n")


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
            cv.acquire()
            cv.wait()
            cv.release()
            print("viz working")
            self.update_data()
            self.gdf['Count'] = self.gdf['ISO2'].map((lambda x: self.places.count(x)))
            # print(self.gdf.sample())
            ax = self.gdf.dropna().plot(column='Count', cmap='Reds', figsize=(16, 10), k=9)
            plt.show()


ports_and_headers = [(2222, "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n"), (2221, "")]
pots = []

for pair in ports_and_headers:
    pots.append(Pot(pair[0], pair[1]))
v = Visualiser(logfile)

for pot in pots:
    pot.start()
v.start()
