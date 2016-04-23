from rest_framework import serializers
from default_inventorys.models import DefaultInventory

class DefaultInventorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    item_number = serializers.IntegerField(max_value=None, min_value=None)
    quantity = serializers.IntegerField(max_value=None, min_value=None)

    class Meta:
        model = DefaultInventory
