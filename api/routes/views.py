from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from routes.models import Route
from cities.models import City
from events.models import Event
from trucks.models import Truck
from truck_route.models import TruckRoute
from serializers import CitySerializer, EventSerializer, TruckSerializer, TruckRouteSerializer
from datetime import datetime, date
import requests
from pytz import timezone
eastern = timezone('US/Eastern')

class Routes(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        routes = Route.objects.all()
        routes_data = []
        for route in routes:
            temp_route_data = {}
            temp_route_data["route_number"] = route.route_number
            temp_route_data["city_labels"] = get_city_labels(route)
            temp_route_data["assigned_truck"] = get_assigned_truck(route)
            temp_route_data["available_trucks"] = get_available_trucks(route)
            temp_route_data["cities"] = get_cities_data(route)
            routes_data.append(temp_route_data)

        return Response(routes_data, status=status.HTTP_200_OK)

    #Update route and truck assignment
    def post(self, request):
        msg = {}
        msg["errors"] = []
        today = datetime.now(eastern).date()
        data = request.data
        print data
        serializer = TruckRouteSerializer(data=data, many=True)
        try:
            if serializer.is_valid():
                data= serializer.validated_data
            else:
                raise Exception("Please make sure the input data is correct")
            
            for assignment in data:
                truck_route = TruckRoute.objects.filter(date_added=today, route_number=assignment["route_number"]).first()
                #if the assignment currently exists then we swap
                if truck_route:
                    truck_route.truck_number = assignment["truck_number"]
                    truck_route.save()
                else:
                    #Otherwise we create a new truck route assignment
                    new_truck_route = {}
                    new_truck_route["truck_number"] = assignment["truck_number"]
                    new_truck_route["route_number"] = assignment["route_number"]
                    new_truck_route["date_added"] = today
                    db_truck_route = TruckRoute.objects.create(**new_truck_route)
        except Exception as e:
            msg["errors"].append(str(e))
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        #Call the get to return updated data
        return self.get(request)

def get_available_trucks(route):
    today = datetime.now(eastern).date()
    truck_routes = TruckRoute.objects.filter(date_added=today).values("truck_number").distinct()
    trucks_assigned = []
    for truck_route in truck_routes:
        trucks_assigned.append(truck_route["truck_number"])
    available_trucks = Truck.objects.exclude(truck_number__in=trucks_assigned)
    serializer = TruckSerializer(available_trucks, many=True)
    return serializer.data

def get_assigned_truck(route):
    today = datetime.now(eastern).date()
    truck_route = TruckRoute.objects.filter(route_number=route.route_number, date_added=today).first()
    #For test purposes
#    truck_route = TruckRoute.objects.filter(route_number=route.route_number).order_by('-date_added').first()
    if truck_route:
        return truck_route.truck_number
    else:
        return None

def get_events(city):
    events = Event.objects.filter(city=city)
    serializer = EventSerializer(events, many=True)
    return serializer.data


def get_city_labels(route):
    cities = City.objects.filter(route=route)
    serializer = CitySerializer(cities, many=True)
    return serializer.data


def get_cities_data(route):
    cities = City.objects.filter(route=route).values("city_name").distinct()
    for city in cities:
        city["events"] = get_events(city["city_name"])
        city["weather"] = get_weather(city["city_name"])
    return cities

def get_weather(city):
    weather_data = {}
    URL = "http://api.openweathermap.org/data/2.5/forecast/daily?APPID=38c5418a7c20bc425e41f0f5f5e11908&cnt=1&q={}&units=Imperial"
    response = requests.get(URL.format(city.lower().strip()))
    if response.status_code == requests.codes.ok:
        weather = response.json()
        weather = weather["list"][0]
        weather_data["condition"] = weather["weather"][0]["main"]
        temp = weather["temp"]
        weather_data["day_temp"] = temp["day"]
        weather_data["min_temp"] = temp["min"]
        weather_data["max_temp"] = temp["max"]
        weather_data["morn_temp"] = temp["morn"]

    return weather_data






