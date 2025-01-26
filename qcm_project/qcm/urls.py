from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-image/', views.process_image, name='process_image'),
]
