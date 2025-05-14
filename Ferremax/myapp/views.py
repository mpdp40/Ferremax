from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm ,RegistroUsuarioForm,LoginForm
from django.contrib.auth import authenticate, login,logout


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

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
        else:
            return render(request, 'registroU.html', {'form': form})
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registroU.html', {'form': form})

def iniciarsession(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def Deslogearse(request):
    logout(request)
    return redirect('login')  