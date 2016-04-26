from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from warehouse_inventory.models import WarehouseInventory
from serializers import WahouseInventorySerializer
import logging
log = logging.getLogger('ice_cream_api')

class WarehouseInventoryView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request, format=None):
        inventory = WarehouseInventory.objects.all()
        serializer = WahouseInventorySerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        msg = {}
        data = request.data
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
                db_inventory = WarehouseInventory.objects.get(id=int(item["id"]))
                try:
                    validate_item(item)
                    #Iterate over the item and update all the changes to the item
                    for key, value in item.iteritems():
                        if key != "id":
                            setattr(db_inventory, key, value)
                    db_inventory.save()
                except Exception as e:
                    error = str(e)
                    log.error(error)
                    msg["errors"].append(error)
        except Exception as e:
            log.error(str(e))
            msg["errors"].append(str(e))
        #Check for errors
        if not msg["errors"]:
            log.info("Updated Warehouse Inventory")
            #Call the get function
            return self.get(request)
        else:
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


#Validate the item
def validate_item(item):
    item_number = item["item_number"]
    print item
    if "description" in item and not item["description"]:
        raise Exception("Description for item {} cannot be empty".format(item_number))
    if "quantity" in item and int(item["quantity"]) < 0:
        raise Exception("Quantity for item {} cannot be negative".format(item_number))
    if "price" in item and float(item["price"]) < 0:
        raise Exception("Price for item {} cannot be negative".format(item_number))




