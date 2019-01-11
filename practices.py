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
  

def display_practices(df, color):
  for index, row in df.iterrows():
    x, y = map(row['x'], row['y'])
    map.plot(x, y, marker='.', markeredgecolor=darken_color(color), color=color, markersize=15)

year = 2018
include_potential = True
output_filename = 'genvasc_2020'

plt.rcParams["font.family"] = "norasi"
fig = plt.figure(figsize=(16, 12))
#fig.suptitle("Title for whole figure", fontsize=48)

gs = gridspec.GridSpec(
  1,
  3,
  width_ratios=[1, 1,10]
)

df_recruitment = pd.read_csv('data/genvasc_recruitment.csv')
df_recruitment = df_recruitment.set_index('year')

ax_recruits = plt.subplot(gs[1])

recruit_count = df_recruitment.loc[year]['cum_recruited']
potential_recruits = 0

if include_potential:
  potential_linc_cam_in_2_years = 8000
  actual_llr_northants_in_last_year = 8000
  potential_recruits += potential_linc_cam_in_2_years + (actual_llr_northants_in_last_year * 2)

plt.title("Recruits")
plt.bar(('Recruits'), recruit_count, align='center', color='#6EBC4F')
plt.bar(('Recruits'), potential_recruits, bottom=recruit_count, align='center', color=darken_color('#6EBC4F'))
plt.yticks(np.arange(0, 75_000, step=10_000))
plt.xticks([])

ax_map = plt.subplot(gs[2])

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
ax_map.add_collection(pc)

df_towns = pd.read_csv('data/towns_geo.csv')

for index, row in df_towns.iterrows():
  x, y = map(row['x'], row['y'])
  txt = ax_map.text(
    x,
    y,
    row['name'].title().replace(' ', '\n'),
    fontsize=16,
    horizontalalignment='center',
    verticalalignment='bottom',
    color='#FFFFFF',
    weight='bold'
  )
  txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='#444444')])


df_genvasc_practices = pd.read_csv('data/genvasc_practices_geo.csv')
df_cam = pd.read_csv('data/cambridgeshire_geo.csv')
df_linc = pd.read_csv('data/our_lincolnshire_geo.csv')

df_genvasc_practices = df_genvasc_practices.loc[df_genvasc_practices['year'] <= year]

practice_count = len(df_genvasc_practices.index)
potential_practice_count = 0

display_practices(df_genvasc_practices, '#F48C38')

if include_potential:
  potential_practice_count = (len(df_cam.index) + len(df_cam.index)) * 0.7
  display_practices(df_cam, '#00AADD')
  display_practices(df_linc, '#DDDD00')

ax_practices = plt.subplot(gs[0])

plt.title("Practices")
plt.bar(('Practices'), practice_count, align='center', color='#006FCA')
plt.bar(('Practices'), potential_practice_count, bottom=practice_count, align='center', color=darken_color('#006FCA'))
plt.yticks(np.arange(0, 550, step=100))
plt.xticks([])

plt.tight_layout()

plt.savefig('{}.png'.format(output_filename))