from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('camera', views.name),
    path('test',views.test),
    path('all',views.all),
    path('only',views.only),
    path('test1',views.camera1),
    path('test2',views.camera2),
    path('test3',views.camera3)
]