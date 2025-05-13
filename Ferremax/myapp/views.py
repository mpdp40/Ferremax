from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm

def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def inventario(request):
    productos = Producto.objects.all()
    return render ( request, 'inventarioLP.html', {'productos': productos})



def EliminarP(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('inventario') 

def agregarP(request):
    form = ProductoForm(request.POST)
    if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        return render(request,'agregarP.html',{'form': form})
    
def editarP(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(request.POST, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)  
    return render(request, 'editarP.html', {'form': form, 'producto': producto})