from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usecases/', views.usecases, name='usecases'),
    path('explore/', views.explore, name='explore'),
]
