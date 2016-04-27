from rest_framework import serializers
from truck_inventory.models import TruckInventory

class TruckInventorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = TruckInventory
        fields = ('id', 'item_number', 'price', 'quantity', 'description', 'truck_number')
