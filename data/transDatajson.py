import osmnx as ox
import json
from math import radians, cos, sin, asin, sqrt

#import các thư viện cần thiết

def haversine(lon1, lat1, lon2, lat2):
    R = 6371 # bán kính trái đất
    dlon = radians(lon2 - lon1) # chuyển sự chênh lệch giữa kinh độ và vĩ độ từ độ sang radian
    dlat = radians(lat2 - lat1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2 # đại lượng trung gian giúp tính góc giữa hai điểm trên hình cầu
    c = 2 * asin(sqrt(a)) # tính góc cung lớn giữa hai điểm bằng công thức lượng giác
    return R * c  # khoảng cách giữa 2 điểm (km)

input_osm = "map.osm"
output_json = "data.json"
G = ox.graph_from_xml(input_osm, simplify=True)
result = {}

for u, v, data in G.edges(data=True):  # duyệt qua các cạnh của đồ thị
    node_u = G.nodes[u]
    node_v = G.nodes[v]
    lat_u, lon_u = node_u['y'], node_u['x']
    lat_v, lon_v = node_v['y'], node_v['x']
    dist = haversine(lon_u, lat_u, lon_v, lat_v)

    key = f"({lat_v}, {lon_v})"
    parent = f"({lat_u}, {lon_u})"
    result[key] = {
        "parent": parent,
        "cost": round(dist, 6)
    }

with open(output_json, "w") as f:
    json.dump(result, f, indent=3)

print(f"Đã lưu vào file: {output_json}")