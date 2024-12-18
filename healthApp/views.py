from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TemperatureSerializer, PulseOximeterSerializer
from django.shortcuts import render,redirect
import smtplib

@api_view(['POST'])
def temperature_create(request):
    serializer = TemperatureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sensor_data_create(request):
    serializer = PulseOximeterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Temperature, PulseOximeter

# def emergency(request):
#     obj = Temperature.objects.all()
#     obj1 = obj.filter(temerature__gt = 30)
    
#     return render(request, 'temperature.html', {'obj': obj1})
def emergency(request):
    #send_email1()
    obj = Temperature.objects.all()
    obj1 = obj.filter(temperature__gt=30)
    # print(type(obj1))
    return render(request, 'emergency.html', {'obj': obj1})

def home(request):
    #send_email1()
    home = "hello "
    return render(request, 'home.html',{'home':home})


def allTemp(request):
    #send_email1()
    objects = Temperature.objects.all().order_by('-timestamp')
    return render(request, 'allTemp.html', {'objects':objects})



def get_last_temperature(request):
    #send_email1()
    last_temp = Temperature.objects.order_by('-timestamp').first()
    #last_temp = Temperature.objects.order_by('timestamp').last()
    return render(request, 'last_temperature.html', {'last_temp': last_temp})

# def get_last_pulseoxy(request):
#     #send_email1()
#     last_pulseoxy = PulseOximeter.objects.order_by('timestamp').last
#     return render(request, 'last_pulseoxy.html', {'po': last_pulseoxy})


def get_last_pulseoxy(request):
    last_pulseoxy = PulseOximeter.objects.order_by('timestamp').last
    return render(request, 'last_pulseoxy.html', {'po': last_pulseoxy})

# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from sklearn.neighbors import KNeighborsClassifier
# def knn_analysis(request):
#     dataset = pd.read_csv(r"C:\Users\Nithin\Desktop\backend\healthProj\health.csv")
#     X=dataset.iloc[:,:2]
#     y=dataset.iloc[:,-1]
#     scaler=StandardScaler()
#     X_1 = scaler.fit_transform(X)
    
#     knn_obj = KNeighborsClassifier(n_neighbors=3);
#     knn_obj.fit(X_1, y)
    
    
    
#     last_pulseoxy = PulseOximeter.objects.order_by('-timestamp').first()
    
#     X_new = np.array([[last_pulseoxy.bpm],[last_pulseoxy.spo2]])
#     X_new = scaler.fit_transform(X_new)
#     outputClass = knn_obj.predict(X_new)
#     return render(request, 'knn_analysis.html', {'outputClass': outputClass,
#                                                  'last_pulseoxy': last_pulseoxy})
    
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from django.shortcuts import render
from .models import PulseOximeter

def knn_analysis(request):
    # Load the dataset
    dataset = pd.read_csv(r"C:\Users\Nithin\Desktop\backend\CSI\healthProj\health.csv")
    
    # Prepare the data
    X = dataset.iloc[:, :2]
    y = dataset.iloc[:, -1]
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train the KNN classifier
    knn_obj = KNeighborsClassifier(n_neighbors=3)
    knn_obj.fit(X_scaled, y)
    
    # Get the latest PulseOximeter reading
    last_pulseoxy = PulseOximeter.objects.order_by('-timestamp').first()
    
    if last_pulseoxy is not None:
        # Prepare the new input for prediction
        X_new = pd.DataFrame([[last_pulseoxy.bpm, last_pulseoxy.spo2]], columns=['bpm', 'spo2'])
        X_new_scaled = scaler.transform(X_new)
        
        # Predict the class for the new input
        outputClass = knn_obj.predict(X_new_scaled)
        outputClass = outputClass[0]  # Extracting the class from the array
    else:
        outputClass = None

    return render(request, 'knn_analysis.html', {
        'outputClass': outputClass,
        'last_pulseoxy': last_pulseoxy
    })


# def chartjsAnalysis(request):
#     a = "a"
#     return render(request, 'chartjs_analysis.html',{"a": a})



import json
from django.shortcuts import render
from .models import Temperature

def chartjsAnalysis(request):
    temperatures = Temperature.objects.all().order_by('timestamp')
    
    x = [temp.timestamp for temp in temperatures]
    y = [temp.temperature for temp in temperatures]
    
    return render(request, 'chartjs_analysis.html', {'x': x, 'y': y})

# def chartjsAnalysis(request):
#     temperatures = Temperature.objects.all().order_by('timestamp')
#     all = Temperature.objects.all()
#     x = all.temperature
#     y= all.timestamp
    
#     return render(request, 'chartjs_analysis.html', {'x': x,'y': y})

   
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
sender= os.getenv('email')
receiver= 'cnithin650@gmail.com'

msg = EmailMessage()
msg['subject'] = 'Medical Emergency'

msg['From'] = os.getenv('email')
msg['To'] = 'cnithin650@gmail.com'



def send_email(request):
    last_temp = Temperature.objects.order_by('-timestamp').first()
    last_pulseoxy = PulseOximeter.objects.order_by('-timestamp').first()
    content = []
    if last_temp.temperature > 37.0:
        content.append(f'High temperature detected {last_temp.temperature}')
    if  last_pulseoxy.bpm < 65.0:
        content.append(f'Low pulse rate detected {last_pulseoxy.bpm}')
    if last_pulseoxy.spo2 < 92.0:
        content.append(f'Low dissolved oxygen {last_pulseoxy.spo2}')
    if content:  # If there's any content to send
        msg.set_content('\n'.join(content))
    
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(os.getenv('email'),os.getenv('password'))
            smtp.send_message(msg)
# def send_email1():
#     last_temp = Temperature.objects.order_by('-timestamp').first()
#     last_pulseoxy = PulseOximeter.objects.order_by('-timestamp').first()
#     content = []
#     if last_temp.temperature > 37.0:
#         content.append(f'High temperature detected {last_temp.temperature}')
#     if  last_pulseoxy.bpm < 65.0:
#         content.append(f'Low pulse rate detected {last_pulseoxy.bpm}')
#     if last_pulseoxy.spo2 < 92.0:
#         content.append(f'Low dissolved oxygen {last_pulseoxy.spo2}')
#     if content:  # If there's any content to send
#         msg.set_content('\n'.join(content))
    
#         with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
#             smtp.login(os.getenv('email'),os.getenv('password'))
#             smtp.send_message(msg)