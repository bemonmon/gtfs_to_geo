import unittest
import geopandas as gpd
from shapely.geometry import Point
import folium

class TestVisualization(unittest.TestCase):
    """
    Unit tests for visualization functions in gtfs_to_geo.visualization.folium_maps
    """

    def test_plot_reachable_stops(self):
        from gtfs_to_geo.visualization.folium_maps import plot_reachable_stops

        # Min GeoDataFrame with one stop
        gdf = gpd.GeoDataFrame(
            {"stop_id": ["stop_1"], "arrival_time_min": [5]},
            geometry=[Point(13.4, 52.5)],
            crs="EPSG:4326"
        )

        origin = (52.5, 13.4)  # lat, lon for folium

        m = plot_reachable_stops(gdf, origin)

        # Check that output is folium.Map
        self.assertIsInstance(m, folium.Map)

        # Check that the origin point is added (marker in the map)
        # Folium stores objects in _children
        markers = [child for child in m._children.values() if isinstance(child, folium.map.Marker)]
        self.assertTrue(any(marker.location == list(origin) for marker in markers))


if __name__ == "__main__":
    unittest.main()