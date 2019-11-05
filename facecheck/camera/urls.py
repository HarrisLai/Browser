from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('camera', views.catch),
    path('test',views.camera)
]