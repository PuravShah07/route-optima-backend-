import math
import heapq


GODOWN_LAT, GODOWN_LON = 23.2156, 72.6369

# ---------- Helper Function ----------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ---------- Graph-Based Optimizer ----------
def optimize_route(cluster):
    # Include godown as the starting node
    nodes = [{'OrderID': 'Godown', 'Latitude': GODOWN_LAT, 'Longitude': GODOWN_LON}] + cluster
    
    n = len(nodes)
    graph = [[0]*n for _ in range(n)]
    
    # Build distance matrix
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(nodes[i]['Latitude'], nodes[i]['Longitude'],
                          nodes[j]['Latitude'], nodes[j]['Longitude'])
            graph[i][j] = graph[j][i] = d

    # --- MST-based traversal (Prim’s Algorithm) ---
    visited = [False]*n
    pq = [(0, 0, -1)]  # (distance, node, parent)
    mst_edges = []
    total = 0

    while pq:
        dist, u, parent = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        total += dist
        if parent != -1:
            mst_edges.append((parent, u, dist))
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                heapq.heappush(pq, (graph[u][v], v, u))

    # --- Convert MST to DFS order for route traversal ---
    adj = [[] for _ in range(n)]
    for u, v, _ in mst_edges:
        adj[u].append(v)
        adj[v].append(u)

    order = []
    visited = [False]*n
    def dfs(u):
        visited[u] = True
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
    dfs(0)  # start from godown

    # Return back to godown at end
    order.append(0)

    # --- Prepare final route ---
    route = [nodes[i] for i in order]
    return route

# ---------- Metrics ----------
def route_metrics(route):
    total_distance = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i + 1]
        dist = haversine(a['Latitude'], a['Longitude'], b['Latitude'], b['Longitude'])
        total_distance += dist
    total_cost = total_distance * 10
    return {'total_distance_km': round(total_distance, 2), 'total_cost_inr': round(total_cost, 2)}
