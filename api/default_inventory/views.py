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
import logging
log = logging.getLogger('ice_cream_api')
from pytz import timezone
eastern = timezone('US/Eastern')

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
        serializer = DefaultInventorySerializer(data=data, many=True)
        try:
            if serializer.is_valid():
                data = serializer.validated_data
            else:
                for error in serializer.errors:
                    if error:
                        for key, value in error.iteritems():
                            msg["errors"].append("{} : {}".format(key, value[0]))
                raise Exception("Please make sure the input data is correct")

            for item in data:
                db_inventory = DefaultInventory.objects.get(id=int(item["id"]))
                try:
                    validate_item(item)
                    for key, value in item.iteritems():
                        if key != "id":
                            setattr(db_inventory, key, value)
                    db_inventory.save()
                except Exception as e:
                    error = str(e)
                    msg["errors"].append(error)
        except Exception as e:
            msg["errors"].append(str(e))
        #Check for errors
        if not msg["errors"]:
            #Call the get function
            return self.get(request)
        else:
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

#Validate the item
def validate_item(item):
    item_number = item["item_number"]
    if "description" in item and not item["description"]:
        raise Exception("Description for item {} cannot be empty".format(item_number))
    if "quantity" in item and int(item["quantity"]) < 0:
        raise Exception("Quantity for item {} cannot be negative".format(item_number))

#Sets the start of the day
class DayStatusView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self, request, format=None):
        msg = {}
        msg["errors"] = []
        msg["result"] = []
        today = datetime.now(eastern).date()
        day_status, created = DayStatus.objects.get_or_create(login_date = today)
        #If they are logging in for the first time as in if the object has been created
        print created
        if created:
            #Used in the real world to start the day and load all the default inventory
#            errors = set_default_truck_inventory(today)
            msg["errors"] = errors
            #Check if there are any errors and return accordingly
            if not errors:
                msg["result"].append("Default inventory has been assigned for today")
            else:
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        # msg["date"] = today
        return Response(msg, status=status.HTTP_200_OK)


#Set the Default Inventory at the start of each day
def set_default_truck_inventory(date):
    errors = []
    default = DefaultInventory.objects.all()
    trucks = Truck.objects.all()
    for truck in trucks:
        truck_number = truck.truck_number
        for item in default:
            db_truck_inventory = {}
            db_truck_inventory["truck_number"] = truck_number
            db_truck_inventory["item_number"] = item.item_number
            #Check if the item is in the warehouse inventory
            try:
                db_item = WarehouseInventory.objects.get(item_number=item.item_number)
            except:
                errors.append("Default inventory item {} not in the warehouse inventory".format(item.item_number))
                continue
            #Save the price for later use
            db_truck_inventory["price"] = db_item.price
            db_truck_inventory["description"] = db_item.description
            #If quantity is greater then the warehouse inventory then assign what is left over
            if item.quantity > db_item.quantity:
                quantity = db_item.quantity
                db_item.quantity = 0
            else:
                quantity = item.quantity
                db_item.quantity -= quantity
            db_item.save()
            db_truck_inventory["quantity"] = quantity
            db_truck_inventory["date_added"] = date
            db_truck_inv = TruckInventory.objects.create(**db_truck_inventory)

    return errors














