from django.contrib import admin
from .models import Producto,DetalleVenta,Venta
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado

admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)


class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    list_display = ['username', 'email', 'first_name', 'last_name', 'fecha_nacimiento', 'telefono']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fecha_nacimiento', 'telefono', 'direccion')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('fecha_nacimiento', 'telefono', 'direccion')}),
    )

admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)