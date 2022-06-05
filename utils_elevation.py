from pathlib import Path

import elevation
import rasterio
from shapely.geometry import LineString

local_dir = Path(__file__).parent
dem_tmp_file = str(local_dir / 'dem_tmp.tif')


def get_dem(track: LineString):
    bounds = track.bounds
    pad = 0.02
    bounds = (bounds[0] - pad, bounds[1] - pad,
              bounds[2] + pad, bounds[3] + pad)
    elevation.clip(bounds=bounds, output=dem_tmp_file, product='SRTM1')

    dem_raster = rasterio.open(dem_tmp_file)
    return dem_raster
