# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/temperature/', views.temperature_create, name='temperature-create'),
    path('api/sensor-data/', views.sensor_data_create, name='sensor-data-create'),
    path('home', views.home, name='home'),
    path('Emergency', views.emergency, name='emergency'),
    path('all_temp', views.allTemp, name='allTemp'),
    path('Tlast', views.get_last_temperature, name='lastTemperature'),
    path('Plast', views.get_last_pulseoxy, name='lastPulseoxy'),
    path("sendemail", views.send_email, name='send'),
    path('knn', views.knn_analysis, name='knn'),
    path('chart', views.chartjsAnalysis, name='chart')
]
