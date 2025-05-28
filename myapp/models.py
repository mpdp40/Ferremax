from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    precio=models.IntegerField()
    cantidad=models.IntegerField()
    def __str__(self):
        return self.nombre

TIPO_Cargos = [
    (0, 'Cliente'),
    (1, 'Vendedor'),
    (2, 'Bodeguero'),
    (3, 'Contador'),
    (4, 'ADMIN'),
]

class UsuarioPersonalizado(AbstractUser):
    Clase=models.IntegerField(choices=TIPO_Cargos, default=0)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

ESTADOS_PEDIDO = [
    (0, 'Recivido'),
    (1, 'Aprobado'),
    (2, 'Enviado'),
    (3, 'Rechazado'),
    (4, 'Preparando'),
]

class Venta(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    direcion= models.CharField(max_length=255)
    estadopedido=models.IntegerField(choices=ESTADOS_PEDIDO, default=0)
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"
    
TIPO_ENVIO_CHOICES = [
    (0, 'Retiro en tienda'),
    (1, 'Envío a domicilio'),
]

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalle', on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precioTotal = models.DecimalField(max_digits=10, decimal_places=2)
    tipoenvio = models.IntegerField(choices=TIPO_ENVIO_CHOICES, default=0)

    def subtotal(self):
        return self.cantidad * self.precioTotal
    
class Pago(models.Model):
    order_id = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.monto}"