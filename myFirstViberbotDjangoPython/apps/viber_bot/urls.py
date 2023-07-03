from django.urls import path
from . import views

urlpatterns = [
    path('incoming/', views.incoming, name='incoming'),
    path('', views.incoming, name='incoming'),
]