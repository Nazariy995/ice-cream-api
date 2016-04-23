from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from default_inventorys.models import DefaultInventory
from serializers import DefaultInventorySerializer

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




