def filter_by_travel_time(gdf, max_minutes):
    return gdf[gdf.arrival_time_min <= max_minutes].copy()
