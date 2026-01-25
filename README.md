# gtfs_to_geo

A Python geospatial library for converting GTFS public transport data into GIS-ready vector formats.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

The library can be used to load and validate a GTFS feed stored in a local folder.

Example:
```bash
from gtfs_to_geo.loader import GTFS
```

## Path to a GTFS feed folder
```bash
gtfs = GTFS("data/sample_gtfs")
```
## Load and validate the GTFS files
```bash
gtfs.load()
```

## Access loaded tables as pandas DataFrames
```bash
stops = gtfs.stops
routes = gtfs.routes
trips = gtfs.trips
stop_times = gtfs.stop_times
```
# Contributing
Contributions are welcome.
## To contribute:

1. Fork the repository
2. Create a new branch for your changes
3. Add or update code and include tests when appropriate
4. Commit your changes with a clear message
5. Open a pull request

