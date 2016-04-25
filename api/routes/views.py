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
from serializers import CitySerializer, EventSerializer, TruckSerializer
from datetime import datetime, date
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

    def post(self, request):
        today = datetime.now(eastern).date()
        data = request.data
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
    return cities

