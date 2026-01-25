# gtfs_to_geo

A Python geospatial library for converting GTFS public transport data into GIS-ready vector formats.

## Installation
```bash
pip install -r requirements.txt

## Usage

The library can be used to load and validate a GTFS feed stored in a local folder.

Example:

```python
from gtfs_to_geo.loader import GTFS

# Path to a GTFS feed folder
gtfs = GTFS("data/sample_gtfs")

# Load and validate the GTFS files
gtfs.load()

# Access loaded tables as pandas DataFrames
stops = gtfs.stops
routes = gtfs.routes
trips = gtfs.trips
stop_times = gtfs.stop_times
