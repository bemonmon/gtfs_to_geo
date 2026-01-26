import folium

def plot_reachable_stops(
    stops_gdf,
    origin,
    time_limit_min=30
):
    """
    Построение карты с reachable stops и точкой origin.
    
    origin: tuple (lat, lon)
    stops_gdf: GeoDataFrame с остановками
    """
    # origin теперь tuple (lat, lon)
    m = folium.Map(
        location=origin,
        zoom_start=14,
        tiles="OpenStreetMap"
    )

    # стартовая точка
    folium.Marker(
        location=origin,
        icon=folium.Icon(color="red", icon="home"),
        tooltip="Origin"
    ).add_to(m)

    # остановки
    for _, row in stops_gdf.iterrows():
        folium.CircleMarker(
            location=(row.geometry.y, row.geometry.x),  # y = lat, x = lon
            radius=4,
            color="blue",
            fill=True,
            fill_opacity=0.7,
            tooltip=f"""
            Stop: {row.stop_id}<br>
            Arrival: {row.arrival_time_min:.1f} min
            """
        ).add_to(m)

    return m
