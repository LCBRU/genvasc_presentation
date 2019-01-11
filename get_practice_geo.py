import pandas as pd
import geocoder


def get_geocoder(location):
    g = geocoder.osm('{}, UK'.format(location))
    if g:
        return g.osm['x'], g.osm['y']
    else:
        return None, None


df = pd.read_csv('data/genvasc_practices.csv')

df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

df.to_csv('data/genvasc_practices_geo.csv')

df = pd.read_csv('data/our_lincolnshire.csv')

df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

df.to_csv('data/our_lincolnshire_geo.csv')

df = pd.read_csv('data/cambridgeshire.csv')

df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

df.to_csv('data/cambridgeshire_geo.csv')