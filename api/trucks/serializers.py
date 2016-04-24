from rest_framework import serializers
from truck_inventory.models import TruckInventory

class TruckInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckInventory
        fields = ('id', 'item_number', 'price', 'quantity')
