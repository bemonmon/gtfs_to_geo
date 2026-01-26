from shapely.geometry import LineString
import geopandas as gpd

def shapes_to_lines(shapes_df):
    lines = []
    for shape_id, g in shapes_df.groupby("shape_id"):
        g = g.sort_values("shape_pt_sequence")
        coords = list(zip(g.shape_pt_lon, g.shape_pt_lat))
        if len(coords) > 1:
            lines.append({
                "shape_id": shape_id,
                "geometry": LineString(coords)
            })
    return gpd.GeoDataFrame(lines, crs="EPSG:4326")