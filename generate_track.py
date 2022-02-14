from geopy.distance import geodesic
import geopandas as gpd
import numpy as np

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

track = gpd.read_file('SW_Coast_Path_Full.json')
track = track.sort_values('title')

fig = figure(x_axis_type="mercator", y_axis_type="mercator",
             tooltips=[('Section', '$name'),
                       ('Distance', '@distance')])
fig.aspect_ratio = 1
fig.match_aspect = True
fig.axis.visible = False

for idx, t in track.iterrows():
    geom = t.geometry
    if geom is not None:
        coords = geom.coords
        distances = [geodesic(t0, t1).km for t0, t1 in
                     zip(coords[:-1], coords[1:])]
        distance = np.sum(distances)
        distance = "{:0.2f} km".format(distance)

        lon = [c[0] for c in coords]
        lat = [c[1] for c in coords]
        source = ColumnDataSource({'x': lon,
                                   'y': lat,
                                   'distance': [distance] * len(lon)})
        fig.line('x', 'y', line_width=1, name=t['title'], source=source)

show(fig)
