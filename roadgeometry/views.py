import overpy
from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import math
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from geopy.distance import geodesic


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
                segment = get_nearby_road_segment(coord)
                for i, j in segment:
                    if (geodesic((i, j), coord).meters > 50):
                        segment.remove((i, j))
                print("Nearby coordinates along the road segment:")
                for i, point in enumerate(segment, 1):
                    print(f"{i}. {point}")
                radius_of_curvature(segment, coord)
            else:
                print("NO")
        else:
            return render(request, 'home.html')
    else:
        return render(request,'home.html')
    return render(request,'home.html')

import overpy
from decimal import Decimal


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
    for point in segment:
        lat_diff = given_point[0] - point[0]
        long_diff = given_point[1] - point[1]
        for point1 in segment:
            if (point != point1):
                lat_diff1 = given_point[0] - point1[0]
                long_diff1 = given_point[1] - point1[1]
                if (lat_diff*lat_diff1 < 0 or long_diff*long_diff1 < 0):
                    points = [point, point1, given_point]
                    radius = calculate_radius(points)
                    print(radius)
                    all_radius.append(radius)

    all_radius.sort()
    if (len(all_radius) % 2 != 0):
        print("ROC at the given point is ", all_radius[len(all_radius) // 2])
    elif (len(all_radius) == 0):
        print("ROC at the given point is ", 0)
    elif (len(all_radius) % 2 == 0):
        print("ROC at the given point is ", (all_radius[len(
            all_radius) // 2] + all_radius[(len(all_radius) // 2) - 1]) / 2)


def calculate_radius(points):
    (lat1, lon1), (lat2, lon2), (lat3, lon3) = points
    d12 = geodesic((lat1, lon1), (lat2, lon2)).meters
    d13 = geodesic((lat1, lon1), (lat3, lon3)).meters
    d23 = geodesic((lat2, lon2), (lat3, lon3)).meters
    s = (d12 + d23 + d13) / 2
    radius = (d12 * d13 * d23) / \
        (4 * (s * (s - d12) * (s - d13) * (s - d23))) ** 0.5
    return radius


def get_road_segment(latitude, longitude, radius=1000):
    # OpenStreetMap API endpoint for retrieving road segments
    api_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    # Sending request to OpenStreetMap API
    response = requests.get(api_url)
    # Checking if request was successful
    if response.status_code == 200:
        data = response.json()
        road_name = data.get('address', {}).get('road', None)
        start_point = (float(data.get('boundingbox', [])[0]),
                       float(data.get('boundingbox', [])[2]))
        end_point = (float(data.get('boundingbox', [])[1]),
                     float(data.get('boundingbox', [])[3]))

        if road_name:
            print(f"Found road segment: {road_name}")
            print(f"Start point: {start_point}")
            print(f"End point: {end_point}")
            return road_name, start_point, end_point
        else:
            print("No road segment found at the given coordinates.")
            return None, None, None
    else:
        print("Failed to retrieve road segment. Please try again later.")
        return None, None, None
