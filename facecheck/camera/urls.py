from django.urls import path
from .import views
from .import catch

urlpatterns = [
    path('camera', catch.camera, name='camera'),
    path('', views.index, name='index')
]