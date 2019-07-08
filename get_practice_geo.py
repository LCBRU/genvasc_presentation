import pandas as pd
import geocoder
import time
import numpy as np

def get_geocoder(location):
    time.sleep(0.5)
    g = geocoder.osm('{}, UK'.format(location))
    if g:
        return g.osm['x'], g.osm['y']
    else:
        return None, None


# df = pd.read_csv('data/genvasc_practices.csv')

# df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

# df.to_csv('data/genvasc_practices_geo.csv')

# df = pd.read_csv('data/our_lincolnshire.csv')

# df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

# df.to_csv('data/our_lincolnshire_geo.csv')

# df = pd.read_csv('data/cambridgeshire.csv')

# df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

# df.to_csv('data/cambridgeshire_geo.csv')

# df = pd.read_csv('data/epraccur.csv', usecols=[0,9], names=['code', 'post_code'])

# df = df[(df.code.str.contains('^[A-H,J-N.P-W,Y]\d'))] # England Codes only
# df = df[df['post_code'].notnull()]
# df['x'] = None
# df['y'] = None

# df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

def index_marks(nrows, chunk_size):
    return range(1 * chunk_size, (nrows // chunk_size + 1) * chunk_size, chunk_size)

def split(df, chunk_size):
    indices = index_marks(df.shape[0], chunk_size)
    return np.split(df, indices)

df = pd.read_csv('data/epraccur_geo.csv')

df_todo = df[df.x.isnull()]
df_done = df[df.x.notnull()]

chunks = split(df_todo, 100)

for i, c in enumerate(chunks):
    time.sleep(10)

    df['x'], df['y'] = zip(*df['post_code'].apply(get_geocoder))

    df = pd.concat([*chunks, df_done])

    print(f'Saving chunk {i + 1} of {len(chunks)}')
    df.to_csv('data/epraccur_geo.csv')
