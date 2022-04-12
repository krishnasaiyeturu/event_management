

from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from event.models import *

from django.contrib.auth.models import User as MainUser

class MainUserSerializer(ModelSerializer):
    class Meta:
        model = MainUser

        fields = '__all__'
    
    def run_validation(self, data):
        print("data",data)
        email = data.get('email', None)
        print("data",data.get('email'))
        if MainUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'errors':'Entered Email ID already Exist'})
        return data

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer

        fields = '__all__'
    
    def to_representation(self, instance):  # For Listing instance
        response = super().to_representation(instance)
        response['is_admin'] = False
        return response



class EventManagerSerializer(ModelSerializer):
    class Meta:
        model = EventManager

        fields = '__all__'
    
    def to_representation(self, instance):  # For Listing instance
        response = super().to_representation(instance)
        response['is_admin'] = True
        return response

class EventTypeSerializer(ModelSerializer):
    class Meta:
        model = EventType

        fields = '__all__'

class VenueSerializer(ModelSerializer):
    class Meta:
        model = Venue

        fields = '__all__'


class EstimatedPriceSerializer(ModelSerializer):
    class Meta:
        model = EstimatedPrice

        fields = '__all__'
    
    def to_representation(self, instance):  # For Listing instance
        response = super().to_representation(instance)
        response['venue'] = instance.venue.name
        response['event_type'] = instance.event_type.name
        return response


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event

        fields = '__all__'
    
    def to_representation(self, instance):  # For Listing instance
        response = super().to_representation(instance)
        response['venue'] = instance.venue.name +'-'+instance.venue.street+','+instance.venue.city+','+instance.venue.state
        response['event_type'] = instance.event_type.name
        response['customer'] = instance.customer.name
        return response