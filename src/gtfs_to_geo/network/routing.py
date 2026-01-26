import heapq
from collections import defaultdict
import geopandas as gpd
from shapely import Point


def find_start_stops(
    stops_gdf: gpd.GeoDataFrame,
    origin: tuple[float, float],
    walk_radius_m: float,
    walk_speed_kmh: float = 4.5,
):
    # метрическая CRS
    metric_crs = "EPSG:32633"

    stops_m = stops_gdf.to_crs(metric_crs)

    origin_point = gpd.GeoSeries(
        [Point(origin)],
        crs="EPSG:4326"
    ).to_crs(metric_crs).iloc[0]

    distances = stops_m.geometry.distance(origin_point)

    reachable = stops_m[distances <= walk_radius_m].copy()

    walk_speed_m_min = walk_speed_kmh * 1000 / 60

    reachable["walk_dist_m"] = distances[reachable.index]
    reachable["walk_time_min"] = reachable["walk_dist_m"] / walk_speed_m_min

    return reachable


def multi_source_dijkstra_limited(edges_by_stop, start_times, max_travel_time_min, departure_time_min):
    """
    Multi-source Dijkstra для reachable stops с жёстким ограничением arrival_time.
    
    edges_by_stop: dict[from_stop] = list of (to_stop, departure_min, arrival_next, trip_id)
    start_times: dict[stop_id] = время прибытия на стартовую остановку (minutes)
    max_travel_time_min: максимальное время путешествия от старта
    departure_time_min: время начала отсчета (например 510 для 08:30)
    """
    latest_allowed_time = departure_time_min + max_travel_time_min
    
    # Инициализация
    best_time = defaultdict(lambda: float('inf'))
    parents = dict()
    pq = []  # очередь для Dijkstra (arrival_time, stop_id)
    
    # Начальные остановки
    for stop_id, t in start_times.items():
        if t <= latest_allowed_time:
            best_time[stop_id] = t
            heapq.heappush(pq, (t, stop_id))
    
    while pq:
        current_time, u = heapq.heappop(pq)
        
        # Пропускаем если уже нашли лучшее время
        if current_time > best_time[u]:
            continue
        
        for edge in edges_by_stop.get(u, []):
            to_stop, dep, arr, trip_id = edge
            
            # Нельзя уехать раньше, чем пришли
            if dep < current_time:
                continue
            
            # Нельзя приехать позже лимита
            if arr > latest_allowed_time:
                continue
            
            # Релаксация
            if arr < best_time[to_stop]:
                best_time[to_stop] = arr
                parents[to_stop] = (u, trip_id)
                heapq.heappush(pq, (arr, to_stop))
    
    return dict(best_time), parents