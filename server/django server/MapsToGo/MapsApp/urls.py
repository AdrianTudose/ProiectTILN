from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home-page'),
    path('aplicatie1',views.aplicatie_1,name="aplicatie1"),
    path('aplicatie2',views.aplicatie_2,name="aplicatie2"),
    path('despre', views.despre, name="despre"),
    path('upload_txt', views.upload_txt, name="upload")
]
