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
