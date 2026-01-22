import pandas as pd
from pathlib import Path


class GTFS:
    """
    Core class for loading and validating a GTFS feed.
    """

    def __init__(self, feed_path):
        self.feed_path = Path(feed_path)

        self.stops = None
        self.routes = None
        self.trips = None
        self.stop_times = None

    def load(self):
        """
        Load required GTFS files into pandas DataFrames.
        """
        self.stops = self._load_file("stops.txt")
        self.routes = self._load_file("routes.txt")
        self.trips = self._load_file("trips.txt")
        self.stop_times = self._load_file("stop_times.txt")

    def _load_file(self, filename):
        file_path = self.feed_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Missing GTFS file: {filename}")
        return pd.read_csv(file_path)
