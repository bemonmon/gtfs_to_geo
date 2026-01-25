import pandas as pd
from pathlib import Path
from .exceptions import MissingGTFSFileError, InvalidGTFSError


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
        Load required GTFS files into pandas DataFrames
        and validate their structure.
        """
        self.stops = self._load_file("stops.txt")
        self.routes = self._load_file("routes.txt")
        self.trips = self._load_file("trips.txt")
        self.stop_times = self._load_file("stop_times.txt")

        self.validate()

    def _load_file(self, filename):
        file_path = self.feed_path / filename
        if not file_path.exists():
            raise MissingGTFSFileError(f"Missing GTFS file: {filename}")
        return pd.read_csv(file_path)

    def validate(self):
        """
        Validate required GTFS tables and columns.
        """
        if self.stops is None:
            raise InvalidGTFSError("GTFS feed not loaded. Call load() first.")

        required_stop_cols = {"stop_id", "stop_lat", "stop_lon"}
        if not required_stop_cols.issubset(self.stops.columns):
            raise InvalidGTFSError("stops.txt is missing required columns")

        if "route_id" not in self.routes.columns:
            raise InvalidGTFSError("routes.txt is missing route_id")

        if "trip_id" not in self.trips.columns:
            raise InvalidGTFSError("trips.txt is missing trip_id")
