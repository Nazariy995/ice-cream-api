from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from warehouse_inventory.models import WarehouseInventory
from serializers import WahouseInventorySerializer

class WarehouseInventoryList(generics.ListAPIView):
    queryset = WarehouseInventory.objects.all()
    permission_classes=(IsAuthenticated,)
    serializer_class = WahouseInventorySerializer
