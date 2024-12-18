# serializers.py
from rest_framework import serializers
from .models import *

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['temperature', 'timestamp']
        
        
class PulseOximeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PulseOximeter
        fields = ['bpm', 'spo2', 'timestamp']