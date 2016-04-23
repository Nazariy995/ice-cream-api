from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from default_inventory.models import DefaultInventory
from serializers import DefaultInventorySerializer

from datetime import datetime, date
from truck_inventory.models import TruckInventory
from day_status.models import DayStatus
from warehouse_inventory.models import WarehouseInventory
from trucks.models import Truck

class DefaultInventoryView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, format=None):
        inventory = DefaultInventory.objects.all()
        serializer = DefaultInventorySerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        msg = {}
        data = request.data
        msg["errors"] = []
        try:
            for item in data:
                db_inventory = DefaultInventory.objects.get(id=int(item["id"]))
                for key, value in item.iteritems():
                    if key != "id":
                        setattr(db_inventory, key, value)
                db_inventory.save()
            msg["result"] = "Updated"
        except Exception as e:
            msg["errors"].append(str(e))
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(msg, status=status.HTTP_200_OK)

#Sets the start of the day
class DayStatusView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, format=None):
        today = date.today()
        day_status, created = DayStatus.objects.get_or_create(login_date = today)
        #if
        if created:
            set_default_truck_inventory(today)

        return Response(status=status.HTTP_200_OK)


#Set the Default Inventory at the start of each day
def set_default_truck_inventory(date):
    default = DefaultInventory.objects.all()
    trucks = Truck.objects.all()
    for truck in trucks:
        truck_number = truck.truck_number
        for item in default:
            db_truck_inventory = {}
            db_truck_inventory["truck_number"] = truck_number
            db_truck_inventory["item_number"] = item.item_number
            db_item = WarehouseInventory.objects.get(item_number=item.item_number)
            db_truck_inventory["price"] = db_item.price
            if item.quantity > db_item.quantity:
                quantity = db_item.quantity
                db_item.quantity = 0
            else:
                quantity = item.quantity
                db_item.quantity -= quantity
            db_item.save()
            db_truck_inventory["quantity"] = quantity

            db_truck_inv = TruckInventory.objects.create(**db_truck_inventory)














