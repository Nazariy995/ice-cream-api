from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from trucks.models import Truck
from truck_inventory.models import TruckInventory
from warehouse_inventory.models import WarehouseInventory
from truck_route.models import TruckRoute
from datetime import datetime, date
from serializers import TruckInventorySerializer
import logging
log = logging.getLogger('ice_cream_api')
from pytz import timezone
eastern = timezone('US/Eastern')

class TruckView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        trucks = Truck.objects.all()
        trucks_data = []
        today = datetime.now(eastern).date()
        print today
        for truck in trucks:
            truck_number = truck.truck_number
            temp_truck_data = {}
            temp_truck_data["truck_number"] = truck_number
            temp_truck_data["route"] =get_route(truck_number, today)
            temp_truck_data["inventory"] = get_inventory(truck_number, today)
            trucks_data.append(temp_truck_data)

        return Response(trucks_data, status=status.HTTP_200_OK)

    #Update Truck inventry
    def post(self, request, format=None):
        msg = {}
        data = request.data
        print data
        serializer = TruckInventorySerializer(data=data, many=True)

        msg["errors"] = []
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
                db_inventory = TruckInventory.objects.get(id=item["id"])
                db_item = WarehouseInventory.objects.get(item_number=item["item_number"])
                try:
                    validate_item(item)
                    #Check the adjustment of the quantity
                    #If the new quantity is lower then previous quantity we need to add to warehouse inventory
                    #If the new quantity is higher we need to take away from the warehouse inventory
                    adjustment = item["quantity"] - db_inventory.quantity
                    if adjustment > db_item.quantity:
                        #assign whatever is in the warehouse inventory
                        adjustment = db_item.quantity
                        #new warehouse inventory = 0
                        db_item.quantity = 0
                    else:
                        #subtract from warehouse inventory
                        db_item.quantity -= adjustment

                    db_inventory.quantity += adjustment
                    db_inventory.save()
                    db_item.save()
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
    if "quantity" in item and int(item["quantity"]) < 0:
        raise Exception("Quantity for item {} cannot be negative".format(item_number))
    if "price" in item and float(item["price"]) < 0:
        raise Exception("Price for item {} cannot be negative".format(item_number))



def get_route(truck_number, date):
    #Get an assigned route if there is one
    try:
        route = TruckRoute.objects.get(truck_number=truck_number, date_added=date)
        return route.route_number
    except Exception as e:
        return None
#    route = TruckRoute.objects.filter(truck_number=truck_number).order_by("-date_added").first()
#    if route:
#        return route.route_number
#    else:
#        return None

#Get all the assigned inventory
def get_inventory(truck_number, date):
    inventory = TruckInventory.objects.filter(truck_number=truck_number, date_added = date)
    serializer = TruckInventorySerializer(inventory, many=True)
    return serializer.data




