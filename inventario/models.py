from django.db import models

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    precio=models.PositiveIntegerField()
    cantidad=models.PositiveIntegerField()
    imagen_url = models.URLField(blank=True, null=True) 
    def __str__(self):
        return self.nombre
