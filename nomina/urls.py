from django.urls import path
from . import views

urlpatterns = [
    path('empleado/perfil/', views.empleado_perfil, name='empleado_perfil'),
    path('  ', views.rrhh_empleados, name='rrhh_empleados'),
    path('rrhh/empleado/<int:id>/editar/', views.rrhh_editar_empleado, name='rrhh_editar_empleado'),
    path('rrhh/crear/', views.rrhh_crear_empleado, name='crear_empleado'),
]
