from rest_framework import serializers
from warehouse_inventory.models import WarehouseInventory

class WahouseInventorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    item_number = serializers.IntegerField(max_value=None, min_value=None)
    quantity = serializers.IntegerField(max_value=None, min_value=None)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField()

    class Meta:
        model = WarehouseInventory
