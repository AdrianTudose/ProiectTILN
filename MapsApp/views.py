from django.shortcuts import render
from Algorithms.main import *
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
    traseu=execute_algorithms("Biserica din cărămidă de la sfârșitul secolului XV-lea, de lângă Palatul Culturii, este Biserica Sf Nicolae. " \
       "O plimbare de 5 minute spre nord, pe Bulevardul Ștefan cel Mare, te duce la Biserica Trei Ierarhi (str. Ștefan " \
       "cel Mare și Sfânt nr. 28).")
   # waypoints_denumiri=['Directia Sanitara Veterinara','Liceul Agronomic']
   # start=[47.748956,26.670367]
   # destinatie=[47.745738,26.674013]
 #waypoints=[47.748131,26.674237,47.747107,26.673049]
    print("*",traseu)
    waypoints=[]
    destinatie=[traseu[-1][0],traseu[-1][1]]
    waypoints_denumiri=[]
    start=[traseu[0][0],traseu[0][1]]
    print("**",destinatie)
    print("**",start)


    for x,y,z in traseu[1:-1]:
        waypoints.append(x)
        waypoints.append(y)
        waypoints_denumiri.append(z)

    print("**",waypoints)


    return render(request,'MapsApp/aplicatie2.html',{'waypoints':waypoints,'start':start,'destinatie':destinatie,'waypoints_denumiri':waypoints_denumiri})
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

