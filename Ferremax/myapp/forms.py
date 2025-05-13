from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad']
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 60}))