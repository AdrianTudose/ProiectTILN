from django.shortcuts import render
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
def aplicatie_2(request):
    start=[47.748956,26.670367]
    destinatie=[47.745738,26.674013]
    waypoints=[47.748131,26.674237,47.747107,26.673049]

    return render(request,'MapsApp/aplicatie2.html',{'waypoints':waypoints,'start':start,'destinatie':destinatie})
def despre(request):
    return render(request,'MapsApp/despre.html')
def upload_txt(request):
    valid=""
    p_class=""
    if request.method=='POST':
     descriere=request.FILES['descriere']
     if check_txt(descriere.name):
         valid="Ati incarcat un fisier txt valid!"
         p_class="text-success"
     else:
         valid="Fiserul incarcat este invalid!"
         p_class="text-warning"
     print(str(descriere.name)+' '+str(descriere.size))

     # getting a local copy
     local_copy = descriere.read().decode('ASCII')
     print(local_copy)

     return render(request,'MapsApp/aplicatie1.html',{'valid':valid,'p_class':p_class})

