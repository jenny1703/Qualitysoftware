from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empleado, Usuario
from django.contrib import admin
from django.contrib.admin.sites import site
from django.template.response import TemplateResponse
from django.contrib.auth.views import LogoutView
from django.utils.dateparse import parse_date

# Vista para permitir logout vía GET (con botón)
class LogoutViewGET(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
def inicio(request):
    return render(request, 'home.html') 

# VISTA DE LOGIN PERSONALIZADA
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔍 Buscar el objeto Usuario relacionado
            try:
                usuario = Usuario.objects.get(user=user)
            except Usuario.DoesNotExist:
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'No se encontró un perfil de usuario asociado.')
                    return redirect('login')

            # ✅ Redireccionar según el rol del modelo Usuario
            if usuario.rol == 'rrhh':
                return redirect('rrhh_empleados')
            elif usuario.rol == 'empleado':
                return redirect('empleado_perfil')
            elif usuario.rol == 'admin':
                return redirect('admin_dashboard')  # Si tienes un dashboard admin personalizado
            else:
                return redirect('dashboard')  # Vista general
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


# VISTA PRINCIPAL QUE REDIRIGE SEGÚN ROL
@login_required
def dashboard(request):
    usuario = get_object_or_404(Usuario, user=request.user)

    if usuario.rol == 'empleado':
        return redirect('empleado_perfil')
    elif usuario.rol == 'rrhh':
        return redirect('rrhh_empleados')
    elif usuario.rol == 'admin':
        return redirect('/admin/')  # Si tu rol 'admin' no es superuser, cámbialo a 'admin_dashboard'
    else:
        messages.error(request, "No tienes un rol asignado.")
        return redirect('login')


# VISTA PERSONALIZADA DEL DASHBOARD DE SUPERUSER
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('dashboard')

    app_list = site.get_app_list(request)

    return TemplateResponse(request, 'admin_dashboard.html', {
        'app_list': app_list
    })

@login_required
def rrhh_crear_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        salario = request.POST.get('salario')
        fecha_ingreso = request.POST.get('fecha_ingreso')  # <--- IMPORTANTE

        # Convertir salario y fecha_ingreso si vienen vacíos
        salario = salario if salario else None
        fecha_ingreso = parse_date(fecha_ingreso)  # Convierte string a date

        Empleado.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            salario=salario,
            fecha_ingreso=fecha_ingreso
        )
        return redirect('rrhh_empleados')

    return render(request, 'rrhh/crear_empleado.html')

# PERFIL DEL EMPLEADO
@login_required
def empleado_perfil(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    if usuario.rol != 'empleado':
        return redirect('dashboard')

    empleado = usuario.empleado

    if request.method == 'POST':
        empleado.telefono = request.POST['telefono']
        empleado.direccion = request.POST['direccion']
        empleado.save()
        messages.success(request, 'Información actualizada.')

    return render(request, 'empleado/perfil.html', {'empleado': empleado})


# RRHH: LISTADO DE EMPLEADOS
@login_required
def rrhh_empleados(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    empleados = Empleado.objects.all()

    return render(request, 'rrhh/lista_empleados.html', {
        'empleados': empleados,
        'usuario': usuario  # 👈 aquí se pasa al template
    })


# RRHH: EDITAR EMPLEADO
@login_required
def rrhh_editar_empleado(request, id):
    usuario = get_object_or_404(Usuario, user=request.user)
    if usuario.rol != 'rrhh':
        return redirect('dashboard')

    empleado = get_object_or_404(Empleado, id=id)

    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.correo = request.POST['correo']
        empleado.telefono = request.POST['telefono']
        empleado.direccion = request.POST['direccion']
        empleado.salario = request.POST['salario']
        empleado.save()
        messages.success(request, 'Empleado actualizado.')
        return redirect('rrhh_empleados')

    return render(request, 'rrhh/editar_empleado.html', {'empleado': empleado})
