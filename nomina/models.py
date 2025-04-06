from django.db import models
from django.contrib.auth.models import User

# Tabla Empleado
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_ingreso = models.DateField() 

    def __str__(self):
        return self.nombre

# Tabla Usuario (extiende el modelo User con un rol y conexión a empleado)
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    
    # Roles posibles: 'empleado', 'rrhh', 'admin'
    ROL_CHOICES = [
        ('empleado', 'Empleado'),
        ('rrhh', 'Recursos Humanos'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

# Tabla Bitácora de cambios en información del empleado
class BitacoraCambios(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    campo_modificado = models.CharField(max_length=50)
    valor_anterior = models.CharField(max_length=255)
    valor_nuevo = models.CharField(max_length=255)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.nombre} modificó {self.campo_modificado}"


class VistaNominaEmpleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'vista_nomina_empleado'


class VistaNominaAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()

    class Meta:
        managed = False
        db_table = 'vista_nomina_admin'
