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


PRACTICE_COLOR = '#22447A'
RECRUIT_COLOR = '#2EA9B0'
DEACTIVATED_COUNTY_COLOR = '#EA5D4E22'
ACTIVATED_COUNTY_COLOR = '#EA5D4E'


def darken_color(color, amount=0.7):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], amount * c[1], c[2])
  

def print_map():
  ax_map = plt.subplot()

  # Map bounding box
  # westlimit=-1.5044; southlimit=52.1023; eastlimit=-0.3151; northlimit=52.8302

  llcrnrlon = -6
  llcrnrlat = 49.8
  urcrnrlon = 2
  urcrnrlat = 56

  map = Basemap(
    resolution='c',
    projection='merc',
    llcrnrlon=llcrnrlon,
    llcrnrlat=llcrnrlat,
    urcrnrlon=urcrnrlon,
    urcrnrlat=urcrnrlat
  )

  map.readshapefile('data/English Ceremonial Counties', 'counties', drawbounds=True)
  counties = [Polygon(np.array(shape), True) for shape in map.counties]

  ax_map.add_collection(
    PatchCollection(
      counties,
      zorder=2,
      facecolors=['#CCCCCC'],
      edgecolor='#FFFFFF',
      linewidths=2.
    )
  )

  df_practices = pd.read_csv('data/epraccur_postcodes.csv', sep='\t')
  df_practices = df_practices[df_practices.Longitude.notnull()]
  df_practices = df_practices[df_practices.Latitude.notnull()]

  df_brcs = pd.read_csv('data/attendees.csv')

  for index, brc in df_brcs.iterrows():
    x, y = map(brc['Longitude'], brc['Latitude'])
    map.plot(x, y, marker='.', color=DEACTIVATED_COUNTY_COLOR, markersize=300)

  for index, practice in df_practices.iterrows():
    x, y = map(practice['Longitude'], practice['Latitude'])

    if any(c.contains_points([[x,y]]) for c in counties):
      map.plot(x, y, marker='.', color=PRACTICE_COLOR, markersize=2)

  for index, brc in df_brcs.iterrows():
    x, y = map(brc['Longitude'], brc['Latitude'])
    map.plot(x, y, marker='.', color=ACTIVATED_COUNTY_COLOR, markersize=20)

plt.rcParams["font.family"] = "lato"
fig = plt.figure(figsize=(16, 12))

print_map()

plt.tight_layout()
plt.savefig('genvasc_national.png')
