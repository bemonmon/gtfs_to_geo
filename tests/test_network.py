import unittest

class TestRoutingFunctions(unittest.TestCase):
    """
    Unit tests for the routing functions in gtfs_to_geo.network.routing.
    Currently tests multi_source_dijkstra_limited with a minimal mock network.
    """

    def setUp(self):
        # Minimal test network with 3 stops
        # format: edges_by_stop[stop] = list of tuples (to_stop, departure_min, arrival_next, travel_time)
        self.edges_by_stop = {
            "stop_1": [("stop_2", 0, 10, 10)],
            "stop_2": [("stop_3", 15, 25, 10)],
            "stop_3": []
        }
        # start time at stop
        self.start_times = {"stop_1": 0}

    def test_dijkstra_limited(self):
        from gtfs_to_geo.network.routing import multi_source_dijkstra_limited

        reachable, parents = multi_source_dijkstra_limited(
            self.edges_by_stop,
            self.start_times,
            max_travel_time_min=30,
            departure_time_min=0
        )

        # Check that reachable includes all stops up to max_travel_time_min
        self.assertIn("stop_2", reachable)
        self.assertIn("stop_3", reachable)
        self.assertLessEqual(reachable["stop_3"], 30)

        # Check that the parent of stop_3 is stop_2
        self.assertEqual(parents["stop_3"][0], "stop_2")  # <-- исправлено


if __name__ == "__main__":
    unittest.main()