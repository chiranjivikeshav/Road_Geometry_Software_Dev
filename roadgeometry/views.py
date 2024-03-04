from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests ,math
import numpy as np

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
                road_segment, start_point, end_point = get_road_segment(latitude, longitude)
                print(road_segment,start_point,end_point)
            else:
                print("NO")
        else:
            return render(request,'home.html')
    else:
        return render(request,'home.html')


def get_road_segment(latitude, longitude, radius=1000):
    # OpenStreetMap API endpoint for retrieving road segments
    api_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    
    # Sending request to OpenStreetMap API
    response = requests.get(api_url)
    
    # Checking if request was successful
    if response.status_code == 200:
        data = response.json()
        road_name = data.get('address', {}).get('road', None)
        start_point = (float(data.get('boundingbox', [])[0]), float(data.get('boundingbox', [])[2]))
        end_point = (float(data.get('boundingbox', [])[1]), float(data.get('boundingbox', [])[3]))
        
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


