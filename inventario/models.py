from django.db import models

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    precio=models.PositiveIntegerField()
    cantidad=models.PositiveIntegerField()
    def __str__(self):
        return self.nombre
