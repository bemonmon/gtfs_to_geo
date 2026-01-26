from collections import defaultdict

def index_edges_by_stop(edges_df):
    """
    Build adjacency list:
    from_stop -> (to_stop, departure_min, arrival_min, travel_time_min)
    """
    adj = defaultdict(list)

    for _, row in edges_df.iterrows():
        adj[row.from_stop].append((
            row.to_stop,
            row.departure_min,
            row.arrival_next,
            row.travel_time_min
        ))

    return adj