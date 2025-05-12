from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inventario', views.inventario, name='inventario'),
    path('eliminar/<int:producto_id>/', views.EliminarP, name='EliminarP'),
]