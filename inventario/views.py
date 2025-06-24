from django.shortcuts import render
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    def create(self, request, *args, **kwargs):
        data = request.data

        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            Producto.objects.bulk_create([Producto(**item) for item in serializer.validated_data])
            return self.list(request)  # devuelve la lista actualizada
        return super().create(request, *args, **kwargs)