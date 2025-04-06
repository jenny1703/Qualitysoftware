from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'  # o asegúrate que 'fecha_ingreso' esté en la lista
