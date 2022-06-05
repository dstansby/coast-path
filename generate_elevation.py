from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

from distance import distance
from utils_elevation import get_dem

tracks = gpd.read_file('SW_Coast_Path_Full.json')
tracks = tracks.sort_values('title')
# Get all Kent walks
kent_idxs = [t.startswith('SW') for t in tracks['title']]
tracks = tracks.iloc[kent_idxs]
# Concatenate all the Kent coordinates
all_coords = LineString(np.row_stack([ls.coords for ls in tracks['geometry']]))

# Get elevation
dem = get_dem(all_coords)
data = dem.read(1)
elev = np.array(list(dem.sample(all_coords.coords)))
# Get distance along track
dist = distance(lon=all_coords.xy[0], lat=all_coords.xy[1])

extent = [dem.bounds[0], dem.bounds[2], dem.bounds[1], dem.bounds[3]]
fig, axs = plt.subplots(nrows=2, ncols=1)

ax = axs[0]
ax.imshow(data, extent=extent, cmap='rainbow')
ax.set_aspect('equal')
ax.plot(*all_coords.xy,
        color='white')

ax = axs[1]
ax.plot(dist, elev)
ax.set_xlabel('Distance (km)')
ax.set_ylabel('m')
plt.show()
