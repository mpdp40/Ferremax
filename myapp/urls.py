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
    path('comprarPedidos/<int:producto_id>/', views.comprarPedidos, name='comprarPedidos'),
    path('vercarrito/', views.vercarrito, name='vercarrito'),
    path('agregar/<int:producto_id>/', views.agregarC, name='agregarC'),
    path('eliminarCarrito/<int:producto_id>/', views.eliminarC, name='eliminarCarrito'),
    path('agregar-venta/', views.agregarVenta, name='agregarVenta'),
    path('Administrar-pedidos/', views.VerPedidos, name='VerPedidos'),
    path('Ordenes/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('Cambiar-estado/<int:venta_id>/', views.Cestado, name='Cestado'),
]