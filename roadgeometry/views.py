import overpy
from decimal import Decimal
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from geopy.distance import geodesic
import numpy as np


def home(request):
    return render(request, 'home.html')


@csrf_exempt
def save_coordinates(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        print(latitude)
        print(longitude)
        osrm_url = f"http://router.project-osrm.org/nearest/v1/driving/{longitude},{latitude}"
        response = requests.get(osrm_url)
        data = response.json()
        if 'code' in data and data['code'] == 'Ok':
            if data['waypoints'][0]['distance'] <= 25:
                print("YES")
                coord = (float(latitude), float(longitude))
                # print(get_road_segment(latitude,longitude))
                segment2 = get_nearby_road_segment(coord)
                for i, j in segment2:
                    if (geodesic((i, j), coord).meters > 50):
                        segment2.remove((i, j))
                print("Nearby coordinates along the road segment:")
                for i, point in enumerate(segment2, 1):
                    print(f"{i}. {point}")
                radius_of_curvature(segment2, coord)
                segment = get_nearby_road_segment(coord, 30, 100)
                ans = find_pt_pc(segment, segment2, coord)
                print(ans[0])
                print(ans[1])
            else:
                print("NO")
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')
    return render(request, 'home.html')


def get_nearby_road_segment(coord, num_points=10, radius=100):
    api = overpy.Overpass()
    lat, lon = map(Decimal, coord)
    bbox = (lat - Decimal('0.01'), lon - Decimal('0.01'),
            lat + Decimal('0.01'), lon + Decimal('0.01'))
    query = f"""
    [out:json];
    way["highway"](around:{radius},{lat},{lon});
    (._;>;);
    out body;
    """
    result = api.query(query)
    road_segment_coords = []
    for way in result.ways:
        for node in way.nodes:
            road_segment_coords.append((float(node.lat), float(node.lon)))
    road_segment_coords.sort(key=lambda c: (
        (c[0] - float(lat))**2 + (c[1] - float(lon))**2)**0.5)
    road_segment_coords = road_segment_coords[:num_points]
    return road_segment_coords


def radius_of_curvature(segment, given_point):
    all_radius = []
    for i in range(len(segment)):
        for j in range(i + 1, len(segment)):
            for k in range(j + 1, len(segment)):
                points = [segment[i], segment[j], segment[k]]
                if not are_points_collinear(points):
                    radius = calculate_radius(points)
                    all_radius.append(radius)

    all_radius = [r for r in all_radius if r is not None]
    if all_radius:
        median_radius = np.median(all_radius)
        print("ROC at the given point is ", median_radius)
    else:
        print("No valid ROC calculated.")
    return median_radius


def are_points_collinear(points):
    (lat1, lon1), (lat2, lon2), (lat3, lon3) = points
    d12 = geodesic((lat1, lon1), (lat2, lon2)).meters
    d13 = geodesic((lat1, lon1), (lat3, lon3)).meters
    d23 = geodesic((lat2, lon2), (lat3, lon3)).meters

    if np.isclose(d12 + d23, d13) or np.isclose(d13 + d12, d23) or np.isclose(d13 + d23, d12):
        return True
    return False


def calculate_radius(points):
    (lat1, lon1), (lat2, lon2), (lat3, lon3) = points
    d12 = geodesic((lat1, lon1), (lat2, lon2)).meters
    d13 = geodesic((lat1, lon1), (lat3, lon3)).meters
    d23 = geodesic((lat2, lon2), (lat3, lon3)).meters
    s = (d12 + d23 + d13) / 2
    radius = (d12 * d13 * d23) / \
        (4 * (s * (s - d12) * (s - d13) * (s - d23))) ** 0.5
    return radius


def find_pt_pc(segment, segment2, given_point):
    left = []
    right = []
    for point in segment:
        distance = geodesic(
            (given_point[0], given_point[1]), (point[0], point[1])).meters
        if point[0] < given_point[0] or (point[0] == given_point[0] and point[1] < given_point[1]):
            left.append((point, distance))
        else:
            right.append((point, distance))

    left = sorted(left, key=lambda x: x[1])
    right = sorted(right, key=lambda x: x[1])

    left = [point[0] for point in left]
    right = [point[0] for point in right]

    given_roc = radius_of_curvature(segment2, given_point)
    pt = None
    for point in left:
        segment3 = get_nearby_road_segment(point)
        point_roc = radius_of_curvature(segment3, point)
        if point_roc is not None and abs(point_roc - given_roc) >= 200.00:
            pt = point
            break

    diff = float('-inf')
    if pt == None:
        for point in left:
            segment3 = get_nearby_road_segment(point)
            point_roc = radius_of_curvature(segment3, point)
            difference = abs(point_roc - given_roc)
            if point_roc is not None and difference > diff:
                diff = difference
                pt = point

    pc = None
    for point in right:
        segment4 = get_nearby_road_segment(point)
        point_roc2 = radius_of_curvature(segment4, point)
        if point_roc2 is not None and abs(point_roc2 - given_roc) >= 200.00:
            pc = point
            break

    diff = float('-inf')
    if pc == None:
        for point in right:
            segment4 = get_nearby_road_segment(point)
            point_roc = radius_of_curvature(segment4, point)
            difference = abs(point_roc - given_roc)
            if point_roc is not None and difference > diff:
                diff = difference
                pc = point

    return pt, pc
