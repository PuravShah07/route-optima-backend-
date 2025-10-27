import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculates distance in kilometers
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))

def optimize_route(cluster):
    # Paid orders first; nearest neighbor for visiting order
    points = cluster.copy()
    route = []
    # Start from first paid order; if none, start from first
    current = next((o for o in points if o['IsPaidDelivery']==1), points[0])
    route.append(current)
    points.remove(current)
    while points:
        # Find nearest point to current
        next_point = min(points, key=lambda o: haversine(
            current['Latitude'], current['Longitude'], o['Latitude'], o['Longitude']))
        route.append(next_point)
        points.remove(next_point)
        current = next_point
    return route

def route_metrics(route):
    total_distance = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i + 1]
        dist = haversine(a['Latitude'], a['Longitude'], b['Latitude'], b['Longitude'])
        total_distance += dist
    # Cost: assume ₹10 per km
    total_cost = total_distance * 10
    return {'total_distance_km': round(total_distance, 2), 'total_cost_inr': round(total_cost, 2)}
