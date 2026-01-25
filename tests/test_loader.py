# Import unittest module to write and run unit tests
import unittest

# Import Path to work with file paths easily
from pathlib import Path

# Import tempfile to create temporary folders for testing
import tempfile

# Import shutil to copy and delete folders and files
import shutil

# Import the GTFS class we want to test
from gtfs_to_geo.loader import GTFS

# Import custom exceptions to check correct error handling
from gtfs_to_geo.exceptions import MissingGTFSFileError, InvalidGTFSError


class TestGTFSLoader(unittest.TestCase):
    """
    Unit tests for the GTFS loader class.
    These tests check that GTFS files are loaded correctly
    and that errors are raised when data is missing or invalid.
    """

    def setUp(self):
        """
        This method runs before each test.
        It defines the path to a valid sample GTFS feed.
        """
        self.sample_feed = Path("data") / "sample_gtfs"

    def test_load_success(self):
        """
        Test that a valid GTFS feed is loaded correctly.
        """

        # Create a GTFS object using the sample GTFS folder
        gtfs = GTFS(self.sample_feed)

        # Load the GTFS feed
        gtfs.load()

        # Check that all GTFS tables were loaded
        self.assertIsNotNone(gtfs.stops)
        self.assertIsNotNone(gtfs.routes)
        self.assertIsNotNone(gtfs.trips)
        self.assertIsNotNone(gtfs.stop_times)

        # Check that stops.txt contains required columns
        self.assertIn("stop_id", gtfs.stops.columns)
        self.assertIn("stop_lat", gtfs.stops.columns)
        self.assertIn("stop_lon", gtfs.stops.columns)

    def test_missing_file_raises_custom_error(self):
        """
        Test that a missing GTFS file raises the correct custom error.
        """

        # Create a temporary directory for testing
        tmp_dir = Path(tempfile.mkdtemp())

        try:
            # Copy the valid sample GTFS feed into the temporary directory
            shutil.copytree(self.sample_feed, tmp_dir / "feed", dirs_exist_ok=True)

            # Remove the required stops.txt file
            (tmp_dir / "feed" / "stops.txt").unlink()

            # Try to load the GTFS feed with a missing file
            gtfs = GTFS(tmp_dir / "feed")

            # Check that the correct exception is raised
            with self.assertRaises(MissingGTFSFileError):
                gtfs.load()

        finally:
            # Remove the temporary directory after the test
            shutil.rmtree(tmp_dir)

    def test_missing_required_column_raises_invalid_error(self):
        """
        Test that missing required columns raise an InvalidGTFSError.
        """

        # Create a temporary directory for testing
        tmp_dir = Path(tempfile.mkdtemp())

        try:
            # Define a temporary GTFS feed folder
            feed_dir = tmp_dir / "feed"

            # Copy the valid sample GTFS feed
            shutil.copytree(self.sample_feed, feed_dir, dirs_exist_ok=True)

            # Overwrite stops.txt with missing stop_lon column
            (feed_dir / "stops.txt").write_text(
                "stop_id,stop_name,stop_lat\n"
                "S1,Stop 1,45.0000\n"
            )

            # Try to load the invalid GTFS feed
            gtfs = GTFS(feed_dir)

            # Check that the correct validation error is raised
            with self.assertRaises(InvalidGTFSError):
                gtfs.load()

        finally:
            # Remove the temporary directory after the test
            shutil.rmtree(tmp_dir)


# Allow running the tests directly from the command line
if __name__ == "__main__":
    unittest.main()
