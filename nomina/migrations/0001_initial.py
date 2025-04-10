# Generated by Django 5.0.14 on 2025-04-06 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VistaNominaAdmin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=100)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_ingreso', models.DateField()),
            ],
            options={
                'db_table': 'vista_nomina_admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VistaNominaEmpleado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'vista_nomina_empleado',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=200)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_ingreso', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BitacoraCambios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo_modificado', models.CharField(max_length=50)),
                ('valor_anterior', models.CharField(max_length=255)),
                ('valor_nuevo', models.CharField(max_length=255)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomina.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('empleado', 'Empleado'), ('rrhh', 'Recursos Humanos'), ('admin', 'Administrador')], max_length=20)),
                ('empleado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nomina.empleado')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
