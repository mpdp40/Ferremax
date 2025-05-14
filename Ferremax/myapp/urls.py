from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inventario', views.inventario, name='inventario'),
    path('agregarP/', views.agregarP, name='agregarP'),
    path('editarP/<int:producto_id>/', views.editarP, name='editarP'),
    path('eliminar/<int:producto_id>/', views.EliminarP, name='EliminarP'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciarsession, name='login'),
    path('Deslogearse/', views.Deslogearse, name='Deslogearse'),

    
]