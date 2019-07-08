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
DEACTIVATED_COUNTY_COLOR = '#FBDFDB'
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
  

def print_map(df_genvasc_practices, df_potential_practices):
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

  activated_counties = [
    'Leicestershire',
    'Northamptonshire',
    'Rutland',
  ]
  deactivated_counties = [
    'Cambridgeshire',
    'Lincolnshire',
  ]

  patches = [Polygon(np.array(shape), True) for info, shape in zip(map.counties_info, map.counties) if info['NAME'] in activated_counties]
  pc = PatchCollection(patches, zorder=2, facecolors=[ACTIVATED_COUNTY_COLOR], edgecolor='#FFFFFF', linewidths=1.)
  ax_map.add_collection(pc)

  patches = [Polygon(np.array(shape), True) for info, shape in zip(map.counties_info, map.counties) if info['NAME'] in deactivated_counties]
  pc = PatchCollection(patches, zorder=2, facecolors=[DEACTIVATED_COUNTY_COLOR], edgecolor='#FFFFFF', linewidths=1.)
  ax_map.add_collection(pc)

  df_towns = pd.read_csv('data/towns_geo.csv')
  df_towns = df_towns[df_towns.name.isin([
    'leicester',
    'loughborough',
    'northampton',
    'kettering',
    'cambridge',
    'peterborough',
    'lincoln',
    'grantham',
    'boston',
    'oakham',
  ])]

  for index, row in df_towns.iterrows():
    x, y = map(row['x'], row['y'])
    txt = ax_map.text(
      x,
      y,
      row['name'].title().replace(' ', '\n'),
      fontsize=26,
      horizontalalignment='left',
      verticalalignment='top',
      color='#222222',
      weight='bold'
    )
    txt.set_path_effects([PathEffects.withStroke(linewidth=6, foreground='#FFFFFF')])

  for index, row in pd.concat([df_genvasc_practices, df_potential_practices]).iterrows():
    x, y = map(row['x'], row['y'])
    map.plot(x, y, marker='.', color=PRACTICE_COLOR, markersize=15)


def print_bar(title, first, second, color, max, step):
  plt.title(title, fontsize=26, y=1.02)
  plt.bar((title), first, align='center', color=color)
  plt.bar((title), second, bottom=first, align='center', color=darken_color(color, 2))
  plt.yticks(np.arange(0, step * round(max/step), step=step), fontsize=20)
  plt.xticks([])


def recruits():
  ax_recruits = plt.subplot(gs[1])

  df_recruitment = pd.read_csv('data/genvasc_recruitment.csv')
  df_recruitment = df_recruitment.set_index('year')

  recruit_count = df_recruitment.loc[year]['cum_recruited']
  potential_recruits = 0

  if include_potential:
    potential_linc_cam_in_2_years = 8000
    actual_llr_northants_in_last_year = 8000
    potential_recruits += potential_linc_cam_in_2_years + (actual_llr_northants_in_last_year * 2)

  print_bar('Recruits', recruit_count, potential_recruits, RECRUIT_COLOR, 75_000, 10_000)


def practices(df_genvasc_practices, df_potential_practices):
  ax_practices = plt.subplot(gs[0])

  practice_count = len(df_genvasc_practices.index)
  potential_practice_count = (0.7 * len(df_potential_practices.index))

  print_bar('Practices', practice_count, potential_practice_count, PRACTICE_COLOR, 600, 100)


year = 2018
include_potential = False
output_filename = 'genvasc_2018'

plt.rcParams["font.family"] = "lato"
fig = plt.figure(figsize=(16, 12))

gs = gridspec.GridSpec(
  1,
  3,
  width_ratios=[1, 1,10]
)

df_genvasc_practices = pd.read_csv('data/genvasc_practices_geo.csv')
df_potential_practices = pd.DataFrame()

if include_potential:
  df_potential_practices = pd.concat([
    pd.read_csv('data/cambridgeshire_geo.csv'),
    pd.read_csv('data/our_lincolnshire_geo.csv'),
  ])

recruits()

print_map(
  df_genvasc_practices[df_genvasc_practices.year <= year],
  df_potential_practices,
)

practices(
  df_genvasc_practices[df_genvasc_practices.year <= year],
  df_potential_practices,
)

plt.tight_layout()
plt.savefig('{}.png'.format(output_filename))
