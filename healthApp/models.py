# models.py
from django.db import models

class Temperature(models.Model):
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temperature: {self.temperature}°C DateTime: {self.timestamp}"
    
class PulseOximeter(models.Model):
    bpm = models.FloatField()
    spo2 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BPM: {self.bpm}, SpO2: {self.spo2}% at {self.timestamp}"