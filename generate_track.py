import itertools

import geopandas as gpd
import numpy as np

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, PanTool, WheelZoomTool
from bokeh.plotting import figure, save

from distance import total_distance

track = gpd.read_file('SW_Coast_Path_Full.json')
track = track.sort_values('title')

pan = PanTool()
wheel = WheelZoomTool()

fig = figure(x_axis_type="mercator", y_axis_type="mercator",
             tooltips=[('Section', '$name'),
                       ('Distance', '@distance')],
             tools=[pan, wheel],
             toolbar_location=None,
             width=600,
             height=300)
fig.aspect_scale = 1
fig.match_aspect = True
fig.axis.visible = False

fig.xgrid.grid_line_color = None
fig.ygrid.grid_line_color = None
fig.outline_line_width = 2
fig.outline_line_color = 'black'

fig.toolbar.active_scroll = wheel
fig.toolbar.active_drag = pan
colors = itertools.cycle(['#e41a1c', '#377eb8', '#4daf4a'])


for idx, t in track.iterrows():
    geom = t.geometry
    if geom is not None:
        coords = geom.coords
        lon = [c[0] for c in coords]
        lat = [c[1] for c in coords]

        d = "{:0.2f} km".format(total_distance(lon=lon, lat=lat))
        source = ColumnDataSource({'x': lon,
                                   'y': np.sin(np.deg2rad(lat)) * lat,
                                   'distance': [d] * len(lon)})
        fig.line('x', 'y', line_width=1.5, name=t['title'], source=source,
                 color=next(colors))

# export_png(fig, filename='map.png', width=1200, height=600)
save(fig, 'index.html', title='England Coast Path Tracks')
