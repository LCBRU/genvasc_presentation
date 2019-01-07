import matplotlib.pyplot as plt
import matplotlib.cm
import pandas as pd
import numpy as np
import itertools

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
from matplotlib import gridspec
import matplotlib.patheffects as PathEffects

f = plt.figure(figsize=(16, 12))

gs = gridspec.GridSpec(
  1,
  2,
  width_ratios=[1,10]
)

df = pd.read_csv('data/genvasc_recruitment.csv')
df = df.set_index('year')

ax0 = plt.subplot(gs[0])

plt.bar(('Recruitment'), [df.loc[2012]['cum_recruited']], align='center')
plt.yticks(np.arange(0, 55_000, step=10_000))
plt.xticks([])

ax1 = plt.subplot(gs[1])

# Map bounding box
# westlimit=-1.5044; southlimit=52.1023; eastlimit=-0.3151; northlimit=52.8302

llcrnrlon = -1.6
llcrnrlat = 51.95
urcrnrlon = 0.6
urcrnrlat = 53.5

map = Basemap(
  resolution='c',
  projection='merc',
  llcrnrlon=llcrnrlon,
  llcrnrlat=llcrnrlat,
  urcrnrlon=urcrnrlon,
  urcrnrlat=urcrnrlat
)

map.readshapefile('data/English Ceremonial Counties', 'counties', drawbounds=False)

local_counties = ('Cambridgeshire', 'Leicestershire', 'Lincolnshire', 'Northamptonshire', 'Rutland')

patches = [Polygon(np.array(shape), True) for info, shape in zip(map.counties_info, map.counties) if info['NAME'] in local_counties]
pc = PatchCollection(patches, zorder=2, facecolors=['#362763', '#00664A', '#362763', '#E62A2C', '#9D0051'], edgecolor='#FFFFFF', linewidths=1.)
ax1.add_collection(pc)

df = pd.read_csv('data/towns_geo.csv')

for index, row in df.iterrows():
  x, y = map(row['x'], row['y'])
  txt = ax1.text(
    x,
    y,
    row['name'].title().replace(' ', '\n'),
    fontsize=14,
    horizontalalignment='center',
    verticalalignment='bottom',
    color='#FFFFFF',
    weight='bold'
  )
  txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='#222222')])


df = pd.read_csv('data/genvasc_practices_geo.csv')

for index, row in df.iterrows():
  x, y = map(row['x'], row['y'])
  map.plot(x, y, marker='o', color='#F48C38', markeredgecolor='#222222', markersize=10)

plt.tight_layout()

plt.savefig('map.png')