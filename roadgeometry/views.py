from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests 
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
            else:
                print("NO")
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve road information'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
