from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto

def inicio(request):
    return render(request, 'index.html')

def inventario(request):
    productos = Producto.objects.all()
    return render ( request, 'inventarioLP.html', {'productos': productos})

def EliminarP(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('inventario') 