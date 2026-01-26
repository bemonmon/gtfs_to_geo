import geopandas as gpd

def build_isochrone_convex_hull(reachable_gdf):
    """
    Build an isochrone polygon using Convex Hull
    from reachable stops.

    Parameters
    ----------
    reachable_gdf : GeoDataFrame
        GeoDataFrame with reachable stops (Point geometries)

    Returns
    -------
    GeoDataFrame
        Single-row GeoDataFrame with isochrone polygon
    """
    merged = reachable_gdf.geometry.unary_union

    hull = merged.convex_hull

    return gpd.GeoDataFrame(
        {"type": ["isochrone"]},
        geometry=[hull],
        crs=reachable_gdf.crs
    )