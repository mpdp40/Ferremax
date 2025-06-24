from django import forms
from .models import Producto, UsuarioPersonalizado
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad']
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 60}))


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'fecha_nacimiento', 'telefono', 'direccion', 'password1', 'password2']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\d+$', str(telefono)):
            raise ValidationError("El número de teléfono debe contener solo dígitos.")
        return telefono
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].widget.attrs.update({
            'type': 'date',
            'class': 'form-control'
        })
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

