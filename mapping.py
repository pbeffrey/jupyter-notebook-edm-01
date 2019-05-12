"""Supports access and processing of GHCN data.

"""

# pylint: disable=invalid-name, locally-disabled
# pylint: disable=pointless-string-statement, locally-disabled

import math
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point  #, Polygon


def latlng_index(lat, lng, mult=1 / 15):
    """Convert latitude and longitude to 'indexes'.

    """
    # 'mult' = 1 / approx-bucket-size-in-deg
    ilat = int(round((lat + 90.0) * mult))
    mult = mult * math.cos(abs(lat) * math.pi / 180.0)
    ilng = int(round((lng + 180.0) * mult))
    return {'latIndex': ilat, 'lngIndex': ilng}


class Mapping:
    """Wraps geopandas.

    """

    def __init__(self):
        """constructor

        """
        self.locations = {'ids': [], 'lats': [], 'lngs': []}
        # latlng_index() currently returns 12x24 buckets, so we
        # need 4 bits for lat and 5 bits for lng. That's 512 buckets.
        self.buckets = [{'list': [], 'data': {}} for i in range(512)]

        path = gpd.datasets.get_path('naturalearth_lowres')
        self.world = gpd.read_file(path)
        # Add a column we'll use later
        self.world['gdp_pp'] = self.world['gdp_md_est'] / self.world['pop_est']

    def add_location(self, loc):
        """Add a {lat, lng} point to be plotted.

        """
        lat = loc['lat']
        lng = loc['lng']
        self.locations['ids'].append(loc['id'])
        self.locations['lats'].append(lat)
        self.locations['lngs'].append(lng)

        index = latlng_index(lat, lng)
        bucket_id = ((index['lngIndex']) << 4) | index['latIndex']
        self.buckets[bucket_id]['list'].append(loc)

    def show(self):
        """Add the geometry and draw the map.

        """
        df = pd.DataFrame({'id': self.locations['ids']})
        geometry = [
            Point(x, y)
            for x, y in zip(self.locations['lngs'], self.locations['lats'])
        ]
        gdf1 = gpd.GeoDataFrame(df, geometry=geometry)

        names = []
        lats = []
        lngs = []
        for i in self.buckets:
            if i['list']:
                names.append('bucket-' + str(i))

                avg_lat = 0
                avg_lng = 0
                for j in i['list']:
                    avg_lat += j['lat']
                    avg_lng += j['lng']

                i['data']['lat'] = avg_lat / len(i['list'])
                i['data']['lng'] = avg_lng / len(i['list'])

                lats.append(i['data']['lat'])
                lngs.append(i['data']['lng'])

        # names = ['' for i in range(len(avg_lat))]
        df = pd.DataFrame({'id': names})
        geometry = [Point(x, y) for x, y in zip(lngs, lats)]
        gdf2 = gpd.GeoDataFrame(df, geometry=geometry)

        ax = self.world.plot(figsize=(15, 7.5), cmap='Pastel1', alpha=0.65)
        gdf1.plot(ax=ax, markersize=0.25, alpha=0.5)
        gdf2.plot(ax=ax, markersize=25.0, alpha=0.25, color='r')

        plt.show()


def _mapping_test():
    """mapping test

    """
    path = gpd.datasets.get_path('naturalearth_lowres')
    world = gpd.read_file(path)
    # df = gpd.read_file(path)

    # Add a column we'll use later
    # df['gdp_pp'] = df['gdp_md_est'] / df['pop_est']

    df = pd.DataFrame({
        'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
        'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
        'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
        'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]
    })
    # Plotted geometry must have the same lenght as the
    # geometry entries in the DataFrame. (!)
    #...
    geometry = [Point(x, y) for x, y in zip(df.Longitude, df.Latitude)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    ax = world.plot(figsize=(15, 7.5), cmap='Pastel1')
    gdf.plot(ax=ax)

    plt.show()


# _mapping_test()
