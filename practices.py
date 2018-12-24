import matplotlib.pyplot as plt
import matplotlib.cm
import pandas as pd
import numpy as np
import geocoder

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

def get_geocoder(postcode):
    g = geocoder.osm('{}, UK'.format(postcode))
    return g.osm['x'], g.osm['y']

fig, ax = plt.subplots(figsize=(10,20))

# df = pd.read_csv('data/genvasc_practices.csv')

# df['x'], df['y'] = zip(*df['postcode'].apply(get_geocoder))

# df.to_csv('data/genvasc_practices_geo.csv')

map = Basemap(
  resolution='l', # c, l, i, h, f or None
  projection='merc',
  lat_0=54.5, lon_0=-4.36,
  llcrnrlon=-6., llcrnrlat= 49.5, urcrnrlon=2., urcrnrlat=55.2)

# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color='coral',lake_color='aqua')
# map.drawcoastlines()
map.readshapefile('data/Areas', 'areas')

df_poly = pd.DataFrame({
        'shapes': [Polygon(np.array(shape), True) for shape in map.areas],
        'area': [area['name'] for area in map.areas_info],
    })

cmap = plt.get_cmap('Oranges')   
pc = PatchCollection(df_poly.shapes, zorder=2)
norm = Normalize()
 
pc.set_facecolor(cmap(norm(df_poly.index)))
ax.add_collection(pc)


df = pd.read_csv('data/genvasc_practices_geo.csv')

for index, row in df.iterrows():
  x, y = map(row['x'], row['y'])
  map.plot(x, y, marker='D', color='m')

plt.show()


# print(df)

plt.savefig('map.png')