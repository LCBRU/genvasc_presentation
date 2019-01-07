import pandas as pd
import geocoder


def get_geocoder(location):
    g = geocoder.osm('{}, UK'.format(location))
    print(g)
    return g.osm['x'], g.osm['y']


df = pd.read_csv('data/towns.csv')

df['x'], df['y'] = zip(*df['name'].apply(get_geocoder))

df.to_csv('data/towns_geo.csv')