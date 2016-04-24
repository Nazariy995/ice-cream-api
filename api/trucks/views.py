from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from trucks.models import Truck
from truck_inventory.models import TruckInventory
from truck_route.models import TruckRoute
from datetime import datetime, date
from serializers import TruckInventorySerializer

class TruckView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        trucks = Truck.objects.all()
        trucks_data = []
        today = date.today()
        for truck in trucks:
            truck_number = truck.truck_number
            temp_truck_data = {}
            temp_truck_data["truck_number"] = truck_number
            temp_truck_data["route"] =get_route(truck_number, today)
            temp_truck_data["inventory"] = get_inventory(truck_number, today)
            trucks_data.append(temp_truck_data)

        return Response(trucks_data, status=status.HTTP_200_OK)


def get_route(truck_number, date):
#    try:
#        route = TruckRoute.objects.get(truck_number=truck_number, date_added=date)
#        return route.route_number
#    except Exception as e:
#        return None
    route = TruckRoute.objects.filter(truck_number=truck_number).order_by("-date_added").first()
    if route:
        return route.route_number
    else:
        return None

def get_inventory(truck_number, date):
    inventory = TruckInventory.objects.filter(truck_number=truck_number, date_added = date)
    serializer = TruckInventorySerializer(inventory, many=True)
    return serializer.data




