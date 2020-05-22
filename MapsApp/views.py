from django.shortcuts import render
from algorithms.main import *
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

from django.views.decorators.csrf import csrf_protect
import json
from django.http import HttpResponse
from django.core import serializers
import logging

#upload functions
def check_txt(file):
    if file.endswith('.txt'):
        return True
    return False
def check_txt(file):
    if file.endswith('.txt'):
        return True
    return False


# Create your views here.
def home(request):
    return render(request,'MapsApp/index.html')
def aplicatie_1(request):
    return render(request,'MapsApp/aplicatie1.html')
def aplicatie_2(request,descriere,oras):
    traseu=execute_algorithms(descriere,oras)
    waypoints=[]
    destinatie=[traseu[-1][0],traseu[-1][1]]
    waypoints_denumiri=[]
    start_finish = []
    start=[traseu[0][0],traseu[0][1]]
    start_finish=[traseu[0][2],traseu[-1][2]]
    print("**",destinatie)
    print("**",start)


    for x,y,z in traseu[1:-1]:
        waypoints.append(x)
        waypoints.append(y)
        waypoints_denumiri.append(z)

    print("**",waypoints)


    return render(request,'MapsApp/aplicatie2.html',{'waypoints':waypoints,'start':start,'destinatie':destinatie,'waypoints_denumiri':waypoints_denumiri,'start_finish':start_finish})
def despre(request):
    return render(request,'MapsApp/despre.html')

def textbox_upload(request):
    descriere=request.POST.get('descriere')
    oras=request.POST.get('orasTextbox')
    #print(descriere)

    return aplicatie_2(request,descriere,oras)

def salveaza_descrierea(f):
    with open('MapsApp/static/MapsApp/descrieri/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return str('MapsApp/static/MapsApp/descrieri/'+f.name)


def textfile_upload(request):
         cale_descriere=salveaza_descrierea(request.FILES['file'])
         with open(cale_descriere, 'r', encoding='utf-8') as file:
          descriere = str(file.read().replace('\n', ''))
          print(descriere)
         oras= oras=request.POST.get('orasUpload')
         print(oras)
         return aplicatie_2(request, descriere, oras)
