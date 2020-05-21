from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home-page'),
    path('aplicatie1',views.aplicatie_1,name="aplicatie1"),
    path('aplicatie2',views.aplicatie_2,name="aplicatie2"),
    path('despre', views.despre, name="despre"),
    path('textbox_upload', views.textbox_upload, name="textbox"),
    path('textfile_upload', views.textfile_upload, name="textfile")
]
