import numpy as np


def distance(*, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """
    Calculate the great circle distance in kilometers between a set of points
    on the earth (specified in decimal degrees).
    """
    lon = np.deg2rad(lon)
    lat = np.deg2rad(lat)

    # haversine formula
    dlon = lon[1:] - lon[:-1]
    dlat = lat[1:] - lat[:-1]
    a = np.sin(dlat/2)**2 + np.cos(lat[:-1]) * np.cos(lat[:-1]) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    dist = np.cumsum(c) * r
    return np.concatenate(([0], dist))


def total_distance(*, lon: np.ndarray, lat: np.ndarray) -> float:
    return distance(lon=lon, lat=lat)[-1]
