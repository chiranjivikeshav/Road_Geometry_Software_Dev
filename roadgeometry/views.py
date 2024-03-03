from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests ,math

def home(request):
    return render(request,'home.html')

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
            # Check if the nearest road is within a certain threshold distance
            if data['waypoints'][0]['distance'] <= 25: 
                 # You can adjust the threshold as needed
                print("YES")
                Find_NearBy(latitude,longitude)
            else:
                print("NO")
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve road information'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def Find_NearBy(latitude, longitude):
    # Query OSRM to get the nearest road point and two nearby points
    osrm_url = f"http://router.project-osrm.org/nearest/v1/driving/{longitude},{latitude}?number=3"
    response = requests.get(osrm_url)
    data = response.json()

    if 'code' in data and data['code'] == 'Ok':
        # Extract the nearest road point and two nearby points
        waypoints = data['waypoints']
        if len(waypoints) >= 3:
            nearest_road_point = waypoints[0]['location']
            nearby_point1 = waypoints[1]['location']
            nearby_point2 = waypoints[2]['location']
            
            print("Nearest road point:", nearest_road_point)
            print("Nearby point 1:", nearby_point1)
            print("Nearby point 2:", nearby_point2)
            point1 = nearest_road_point
            point2 = nearby_point1
            point3 = nearby_point2
            radius = radius_of_curvature(point1[0],point1[1], point2[0],point2[1], point3[0],point3[1])
            print("Radius of curvature:", radius)
            return nearest_road_point, nearby_point1, nearby_point2
        else:
            # If there are not enough nearby points found
            return None, None, None
    else:
        # If failed to retrieve road information
        return None, None, None


def radius_of_curvature(lat1, lon1, lat2, lon2, lat3, lon3):
    # Convert latitudes and longitudes to distances in meters
    d12 = haversine_distance(lat1, lon1, lat2, lon2)
    d23 = haversine_distance(lat2, lon2, lat3, lon3)
    d13 = haversine_distance(lat1, lon1, lat3, lon3)

    # Calculate semi-perimeter
    s = (d12 + d23 + d13) / 2

    # Calculate radius of curvature using Heron's formula
    area = math.sqrt(s * (s - d12) * (s - d23) * (s - d13))
    r = (d12 * d23 * d13) / (4 * area)
    
    return r

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of the Earth in meters
    R = 6371000  # Radius of the Earth in meters
    return R * c