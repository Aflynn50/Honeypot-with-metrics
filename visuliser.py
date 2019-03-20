import requests
import os

import matplotlib.pyplot as plt
import pandas as pd
# import pycountry as pyc
import geopandas as gpd
import descartes

class Visualiser():
    def __init__(self, logfile):
        self.places = []
        self.logfile = logfile
        self.api_key = "7424304154661ba7476d457c0adb3a1a"
        self.ip_getter = "http://api.ipstack.com/{0}?access_key={1}&fields=country_code"
        self.shapefile = "TM_WORLD_BORDERS-0.3.shp"

    def get_data(self):
        with open(self.logfile) as log:
            for line in log:
                url = self.ip_getter.format(str(line), self.api_key)
                self.places.append(requests.get(url).json()['country_code'])  # Fetch country code of IPs in file
            #self.places = list(map((lambda y: pyc.countries.get(alpha_2=y).alpha_3), self.places))
            print(self.places)

    def viz(self):
        #print(gpd.read_file(self.shapefile).sample(5))
        gdf = gpd.read_file(self.shapefile)[['ISO2', 'geometry']].to_crs('+proj=robin')
        gdf['Count'] = gdf['ISO2'].map((lambda x: self.places.count(x)))
        print(gdf.sample())
        ax = gdf.dropna().plot(column='Count', cmap='Reds', figsize=(16, 10), k=9)
        plt.show()


x = Visualiser('ips.txt')
x.get_data()
x.viz()
