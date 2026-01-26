import geopandas as gpd
from shapely.geometry import Point

def stops_to_gdf(stops_df, crs="EPSG:4326"):
    """
    Convert GTFS stops DataFrame to a GeoDataFrame.

    Parameters
    ----------
    stops_df : pandas.DataFrame
        DataFrame containing GTFS stops.txt data
    crs : str, optional
        Coordinate Reference System, default is EPSG:4326 (WGS84)

    Returns
    -------
    geopandas.GeoDataFrame
    """
    required_cols = {"stop_lat", "stop_lon"}

    if not required_cols.issubset(stops_df.columns):
        raise ValueError("stops_df must contain stop_lat and stop_lon columns")

    geometry = [
        Point(lon, lat)
        for lon, lat in zip(stops_df["stop_lon"], stops_df["stop_lat"])
    ]

    gdf = gpd.GeoDataFrame(
        stops_df.copy(),
        geometry=geometry,
        crs=crs
    )

    return gdf

def build_reachable_stops_gdf(stops_gdf, reachable_dict):
    """
    stops_gdf: GeoDataFrame со всеми stops
    reachable_dict: {stop_id: arrival_time_min}
    """

    df = stops_gdf.copy()

    # add time columns
    df["arrival_time_min"] = df["stop_id"].map(reachable_dict)

    # leave only reachable
    df = df.dropna(subset=["arrival_time_min"])

    return df