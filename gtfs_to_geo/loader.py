# Import pandas to read GTFS CSV files into tables (DataFrames)
import pandas as pd

# Import Path to handle file paths in a clean and cross-platform way
from pathlib import Path

# Import custom exceptions defined for GTFS-related errors
from .exceptions import MissingGTFSFileError, InvalidGTFSError


class GTFS:
    """
    Core class for loading and validating a GTFS feed.
    This class handles reading GTFS files and checking their structure.
    """

    def __init__(self, feed_path):
        # Convert the provided path to a Path object
        self.feed_path = Path(feed_path)

        # Initialize GTFS tables as None (they will be loaded later)
        self.stops = None
        self.routes = None
        self.trips = None
        self.stop_times = None
        self.agency = None
        self.shapes = None
        self.frequencies = None
        self.calendar = None
        self.transfers = None

    def load(self):
        """
        Load required GTFS files into pandas DataFrames
        and validate their structure.
        """

        # Load stops.txt file
        self.stops = self._load_file("stops.txt")

        # Load routes.txt file
        self.routes = self._load_file("routes.txt")

        # Load trips.txt file
        self.trips = self._load_file("trips.txt")

        # Load stop_times.txt file
        self.stop_times = self._load_file("stop_times.txt")

        # Load agency.txt file
        self.agency = self._load_file("agency.txt")

        # Load shapes.txt file
        self.shapes = self._load_file("shapes.txt")

        # Load frequencies.txt file
        self.frequencies = self._load_file("frequencies.txt")

        # Load calendar.txt file
        self.calendar = self._load_file("calendar.txt")

        # Load transfers.txt file
        self.transfers = self._load_file("transfers.txt")

        # After loading all files, validate their content
        self.validate()

    def _load_file(self, filename):
        """
        Internal helper method to load a single GTFS file.
        """

        # Build the full path to the GTFS file
        file_path = self.feed_path / filename

        # Check if the file exists
        if not file_path.exists():
            # Raise a custom error if the file is missing
            raise MissingGTFSFileError(f"Missing GTFS file: {filename}")

        # Read the CSV file and return it as a pandas DataFrame
        return pd.read_csv(file_path)

    def validate(self):
        """
        Validate required GTFS tables and columns.
        """

        # Check that the GTFS feed has been loaded
        if self.stops is None:
            raise InvalidGTFSError("GTFS feed not loaded. Call load() first.")

        # Required columns for stops.txt
        required_stop_cols = {"stop_id", "stop_lat", "stop_lon"}

        # Check that stops.txt contains required columns
        if not required_stop_cols.issubset(self.stops.columns):
            raise InvalidGTFSError("stops.txt is missing required columns")

        # Check that routes.txt contains route_id column
        if "route_id" not in self.routes.columns:
            raise InvalidGTFSError("routes.txt is missing route_id")

        # Check that trips.txt contains trip_id column
        if "trip_id" not in self.trips.columns:
            raise InvalidGTFSError("trips.txt is missing trip_id")
