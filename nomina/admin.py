from django.contrib import admin
from .models import Empleado, Usuario, BitacoraCambios, VistaNominaEmpleado, VistaNominaAdmin


# ---------- ADMIN EMPLEADO ----------
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'salario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs  

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# ---------- BITÁCORA CAMBIOS ----------
class BitacoraCambiosAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'campo_modificado', 'valor_anterior', 'valor_nuevo', 'fecha_modificacion')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs  

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# ---------- ADMIN VISTA NOMINA EMPLEADO ----------
class VistaNominaEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'direccion')  

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs 

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ---------- REGISTRO DE MODELOS ----------
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Usuario)
admin.site.register(BitacoraCambios, BitacoraCambiosAdmin)
admin.site.register(VistaNominaEmpleado, VistaNominaEmpleadoAdmin)
admin.site.register(VistaNominaAdmin)  