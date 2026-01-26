from gtfs_to_geo.time_utils import gtfs_time_to_minutes

def build_stop_time_edges(stop_times_df):
    """
    Build temporal edges between consecutive stops for each trip.

    Parameters
    ----------
    stop_times_df : pandas.DataFrame
        GTFS stop_times.txt table

    Returns
    -------
    pandas.DataFrame
        Edges with travel times between stops
    """

    required = {
        "trip_id",
        "stop_id",
        "stop_sequence",
        "arrival_time",
        "departure_time"
    }

    if not required.issubset(stop_times_df.columns):
        raise ValueError("stop_times_df missing required GTFS columns")

    df = stop_times_df.copy()

    # Convert GTFS times to minutes
    df["arrival_min"] = df["arrival_time"].apply(gtfs_time_to_minutes)
    df["departure_min"] = df["departure_time"].apply(gtfs_time_to_minutes)

    # Sort correctly inside each trip
    df = df.sort_values(["trip_id", "stop_sequence"])

    # Shift to get next stop in the same trip
    df["to_stop"] = df.groupby("trip_id")["stop_id"].shift(-1)
    df["arrival_next"] = df.groupby("trip_id")["arrival_min"].shift(-1)

    # Remove last stop of each trip (no outgoing edge)
    edges = df.dropna(subset=["to_stop"]).copy()

    # Build edge table
    edges = edges.rename(columns={"stop_id": "from_stop"})

    edges["travel_time_min"] = (
        edges["arrival_next"] - edges["departure_min"]
    )

    # Remove broken / negative edges
    edges = edges[edges["travel_time_min"] >= 0]
    print('Count of removed negative edges', edges[edges["travel_time_min"] < 0].shape[0])

    return edges[[
        "trip_id",
        "from_stop",
        "to_stop",
        "departure_min",
        "arrival_next",
        "travel_time_min"
    ]]