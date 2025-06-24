from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto,Venta, DetalleVenta
from .forms import ProductoForm ,RegistroUsuarioForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponseForbidden
from functools import wraps
import requests

TIPO_Cargos = [
    (0, 'Cliente'),
    (1, 'Vendedor'),
    (2, 'Bodeguero'),
    (3, 'Contador'),
    (4, 'ADMIN'),
]

NOMBRE_A_CODIGO_CARGO = {nombre.lower(): codigo for codigo, nombre in TIPO_Cargos}

def cargo_requerido(*nombres_cargos):
    if len(nombres_cargos) == 1 and isinstance(nombres_cargos[0], (list, tuple)):
        nombres_cargos = nombres_cargos[0]
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            cargos_permitidos = []
            for nombre in nombres_cargos:
                if isinstance(nombre, str):
                    codigo = NOMBRE_A_CODIGO_CARGO.get(nombre.lower())
                    if codigo is not None:
                        cargos_permitidos.append(codigo)
                else:pass
            if request.user.is_authenticated and request.user.Clase in cargos_permitidos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Acceso denegado.")
        return _wrapped_view
    return decorador

def inicio(request):
    url = 'http://localhost:8000/api/inventario/productos/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        productos = response.json()
    except requests.RequestException as e:
        productos = []
        messages.error(request, f'No se pudieron cargar los productos: {e}')
    
    return render(request, 'index.html', {'productos': productos})
@cargo_requerido('ADMIN','Bodeguero')
def inventario(request):
    url = 'http://localhost:8000/api/inventario/productos/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        productos = response.json()
    except requests.RequestException as e:
        productos = []
        messages.error(request, f'No se pudieron cargar los productos: {e}')
    
    return render(request, 'inventarioLP.html', {'productos': productos})
@cargo_requerido('ADMIN','Vendedor','Contador','Bodeguero')
def VerPedidos(request):
    ventas = Venta.objects.select_related('cliente').annotate(
        total_venta=Sum('detalle__precioTotal')
    )
    return render(request, 'VerPerdidos.html', {'ventas': ventas})
@cargo_requerido('ADMIN')
def EliminarP(request, producto_id):
    api_url = f'http://localhost:8000/api/inventario/productos/{producto_id}/'
    requests.delete(api_url)
    return redirect('inventario')
@cargo_requerido('ADMIN')
def agregarP(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                'nombre': data['nombre'],
                'descripcion': data['descripcion'],
                'precio': data['precio'],
                'cantidad': data['cantidad'],
            }
            requests.post('http://localhost:8000/api/inventario/productos/', json=payload)
            return redirect('inventario')
    else:
        form = ProductoForm()
    return render(request, 'agregarP.html', {'form': form})
@cargo_requerido('ADMIN','Bodeguero') 
def editarP(request, producto_id):
    api_url = f'http://localhost:8000/api/inventario/productos/{producto_id}/'
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                'nombre': data['nombre'],
                'descripcion': data['descripcion'],
                'precio': data['precio'],
                'cantidad': data['cantidad'],
            }
            requests.put(api_url, json=payload)
            return redirect('inventario')
    else:
        response = requests.get(api_url)
        if response.status_code == 200:
            producto_data = response.json()
            form = ProductoForm(initial=producto_data)
        else:
            form = ProductoForm()
    return render(request, 'editarP.html', {'form': form, 'producto_id': producto_id})

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
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

def comprarPedidos(request, producto_id):
    api_url = f'http://localhost:8000/api/inventario/productos/{producto_id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        producto_data = response.json()
        form = ProductoForm(initial=producto_data)
    else:
        form = ProductoForm()
        producto_data = {}
    return render(request, 'ComprarProducto.html', {'form': form, 'producto': producto_data})

def agregarC(request, producto_id):
    api_url = f'http://localhost:8000/api/inventario/productos/{producto_id}/'
    response = requests.get(api_url)

    if response.status_code == 200:
        carrito = request.session.get('carrito', {})
        carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
        request.session['carrito'] = carrito

    next_url = request.GET.get('next', 'vercarrito')
    return redirect(next_url)

def vercarrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        api_url = f'http://localhost:8000/api/inventario/productos/{producto_id}/'
        response = requests.get(api_url)
        if response.status_code == 200:
            producto_data = response.json()
            precio = producto_data.get('precio', 0)
            subtotal = precio * cantidad
            total += subtotal
            productos.append({
                'producto': producto_data,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        else:
            pass

    context = {
        'total_compra': f"{total:.2f}"
    }
    return render(request, 'Carrito.html', {'productos': productos, 'total': total})

def eliminarC(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('vercarrito')
@csrf_exempt
def agregarVenta(request):
    if request.method == 'POST':
        user = request.user
        direccion = request.POST.get('direccion')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')
        precios = request.POST.getlist('precio_total[]')
        tipoenvio = int(request.POST.get('tipoenvio'))
        transaction_id = request.POST.get('paypal_transaction_id')

        venta = Venta.objects.create(cliente=user, direcion=direccion, paypal_transaction_id=transaction_id)

        for i in range(len(productos)):
            nombre_producto = productos[i]
            cantidad_vendida = int(cantidades[i])
            url = f'http://localhost:8000/api/inventario/productos/?nombre={nombre_producto}'
            response = requests.get(url)
            producto_data = None
            if response.status_code == 200:
                resultados = response.json()
                items = resultados.get('results', resultados) if isinstance(resultados, dict) else resultados
                for item in items:
                    if item['nombre'] == nombre_producto:
                        producto_data = item
                        break
            DetalleVenta.objects.create(
                venta=venta,
                producto=nombre_producto,
                cantidad=cantidad_vendida,
                precioTotal=float(precios[i]),
                tipoenvio=tipoenvio
            )
        request.session['carrito'] = {}
        request.session.modified = True
        return redirect('inicio')

    return redirect('vercarrito')
@cargo_requerido('ADMIN','Vendedor','Contador','Bodeguero')
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalle.all()
    return render(request, 'detallespedidos.html', {
        'venta': venta,
        'detalles': detalles
    })
@cargo_requerido('ADMIN','Vendedor','Bodeguero')
def Cestado(request, venta_id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=venta_id)  
        estado = int(request.POST.get('estadopedido')) 
        venta.estadopedido=estado
        venta.save()
        return redirect('detalle_venta', venta_id=venta_id)
    else:
        return redirect('detalle_venta', venta_id=venta_id)
@cargo_requerido('ADMIN','Vendedor')
def E_detalle_envio(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta_id = detalle.venta.id
    venta = detalle.venta
    detalle.delete()
    if not venta.detalle.exists():
        venta.delete()
        return redirect('VerPedidos')
    else:
        return redirect('detalle_venta', venta_id=venta_id)

def Editar_envio(request, detalle_id):
    if request.method == 'POST':
        Ventas = get_object_or_404(DetalleVenta, id=detalle_id)
        tipo = int(request.POST.get('tipoenvio'))
        Ventas.tipoenvio=tipo
        Ventas.save()
        return redirect('detalle_venta', venta_id=Ventas.venta.id)
    else:
        return redirect('detalle_venta', venta_id=Ventas.venta.id)

















