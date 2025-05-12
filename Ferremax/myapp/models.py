from django.db import models

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    precio=models.IntegerField()
    cantidad=models.IntegerField()
    def __str__(self):
        return self.nombre
    
