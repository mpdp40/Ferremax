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


class venta(models.Model):
    id_cliente=models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(venta, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precioTotal = models.DecimalField(max_digits=10, decimal_places=2)
    direcion= models.CharField()
    tipoenvio=models.IntegerField()
    estadopedido=models.IntegerField()

    def subtotal(self):
        return self.cantidad * self.precio_unitario