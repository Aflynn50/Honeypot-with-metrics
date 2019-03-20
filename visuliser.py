import requests
import os

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

class visualiser():
    def __init__(self, logfile):
        self.places = []
        self.logfile = logfile
        self.api_key = "7424304154661ba7476d457c0adb3a1a"
        self.ip_getter = "http://api.ipstack.com/{0}?access_key={1}&fields=country_code"
        self.shapefile = "ne_10m_admin_0_countries.shp"

    def get_data(self):
        with open(self.logfile) as log:
            for line in log:
                url = self.ip_getter.format(str(line), self.api_key)
                self.places.append(requests.get(url)['country_code'])  # Fetch country code of IPs in file

    def viz(self):
        gdf = gpd.read_file(self.shapefile)[['ADM0_A3', 'geometry']].to_crs('+proj=robin')
        df = pd.DataFrame(data={'Country Code':self.places})

        colour_map = plt.get_cmap('Reds')
        scheme = [colour_map(i / 9) for i in range(9)]




