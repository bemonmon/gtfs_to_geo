# gtfs_to_geo

Python library for converting GTFS data to geospatial formats and performing
network-based accessibility analysis.

The library is designed for academic and research use and provides utilities
to load, validate, process and visualize GTFS feeds using standard Python
geospatial tools.

---

## Features

- Load and validate GTFS feeds from a local folder
- Convert GTFS stops and shapes to geospatial objects
- Build transit networks from GTFS data
- Perform simple network-based accessibility analysis
- Visualize reachable stops and isochrones on interactive maps

---

## Installation

This package is **not published on PyPI** and therefore cannot be installed via
`pip install gtfs-to-geo`.

To use the library, clone the repository and install it in editable mode:
```bash
git clone https://github.com/your-username/gtfs_to_geo.git
cd gtfs_to_geo
pip install -e .
```

### Download GTFS data

For proper functionality, you need to download GTFS data for Berlin:

1. Visit https://unternehmen.vbb.de/digitale-services/datensaetze/
2. Download the GTFS dataset for Berlin
3. Extract the ZIP archive to the `data/berlin_gtfs` folder in the project directory
```bash
mkdir -p data/berlin_gtfs
# Extract downloaded ZIP file here
```

---

## Usage

The library can be used to load, validate and process a GTFS feed stored in a
local folder.

---

### Load and validate a GTFS feed
```python
from gtfs_to_geo.loader.loader import GTFS

gtfs = GTFS("data/berlin_gtfs")
gtfs.load()
```

### Access loaded GTFS tables

After loading, the GTFS tables are available as pandas DataFrames:
```python
stops = gtfs.stops
routes = gtfs.routes
trips = gtfs.trips
stop_times = gtfs.stop_times
```

### Network-based accessibility analysis

The library provides tools for public transport accessibility analysis based on
GTFS schedules and a time-dependent routing approach.

Accessibility is computed by propagating travel times through the public
transport network using scheduled departure and arrival times, starting from
one or multiple origin stops.

Example of running a limited multi-source Dijkstra algorithm to compute
reachable stops within a given time budget:
```python
from gtfs_to_geo.network.routing import multi_source_dijkstra_limited

reachable_times, parents = multi_source_dijkstra_limited(
    edges_by_stop,
    start_times,
    max_travel_time_min=30
)
```

### Visualization

Reachable stops can be visualized using interactive maps based on the
**Folium** library.
```python
from gtfs_to_geo.visualization.folium_maps import plot_reachable_stops

m = plot_reachable_stops(
    reachable_gdf,
    origin=(52.52, 13.40)  # (lat, lon)
)

m.save("reachable_stops.html")
```

### Testing

Unit tests are implemented using the built-in `unittest` framework.

To run all tests:
```bash
python -m unittest discover -s tests -p "test_*.py"
```