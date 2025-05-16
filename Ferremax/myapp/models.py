from django.db import models
from django.contrib.auth.models import AbstractUser

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    precio=models.IntegerField()
    cantidad=models.IntegerField()
    def __str__(self):
        return self.nombre
    
class UsuarioPersonalizado(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)


class Venta(models.Model):
    id_cliente=models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    direcion= models.CharField(max_length=255)
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalle', on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precioTotal = models.DecimalField(max_digits=10, decimal_places=2)
    tipoenvio=models.IntegerField()
    estadopedido=models.IntegerField()

    def subtotal(self):
        return self.cantidad * self.precioTotal