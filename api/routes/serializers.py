from rest_framework import serializers
from cities.models import City
from events.models import Event
from trucks.models import Truck

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('city_label', 'city_name', 'state')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('city', 'name', 'date')

class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'truck_number')
