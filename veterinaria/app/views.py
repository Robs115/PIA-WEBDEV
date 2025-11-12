from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita_Veterinaria, Servicio
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


def index(request):
    citas = Cita_Veterinaria.objects.all()
    servicios = Servicio.objects.all()
    return render(request, 'index.html', {"servicios":servicios})


def login(request):
    return render(request, 'login.html')

@login_required
def listar_Cita_Veterinaria(request):
    citas = Cita_Veterinaria.objects.all()
    return render(request, 'listar.html', {'citas': citas})

@login_required
def crear_Cita_Veterinaria(request):
    if request.method == 'POST':
        nombre_dueño = request.POST['nombre_dueño'].upper()
        nombre_mascota = request.POST['nombre_mascota'].upper()
        especie = request.POST['especie'].upper()
        fecha_cita = request.POST['fecha_cita']
        hora_cita = request.POST['hora_cita']
        estatus_cita = request.POST['estatus_cita'].upper()
        descripcion = request.POST['descripcion'].upper()
        servicio_id = request.POST['servicio']
        servicio = Servicio.objects.get(id=servicio_id)

        try:
            fecha_cita_dt = datetime.strptime(fecha_cita, "%Y-%m-%d").date()
            hora_cita_dt = datetime.strptime(hora_cita, "%H:%M").time()
        except ValueError:
            messages.error(request, "Formato de fecha u hora inválido.")
            return redirect('crear')

        # Valida que la fecha no sea anterior a hoy
        hoy = datetime.now().date()
        if fecha_cita_dt < hoy:
            messages.error(request, "No puedes registrar una cita en una fecha anterior a hoy.")
            return redirect('crear')

        # Valida que no haya una cita con la misma fecha y hora
        if Cita_Veterinaria.objects.filter(fecha_cita=fecha_cita_dt, hora_cita=hora_cita_dt).exists():
            messages.error(request, "Ya existe una cita en esa misma fecha y hora.")
            return redirect('crear')

        # Validar intervalo de 30 minutos entre las citas
        hora_actual = datetime.combine(fecha_cita_dt, hora_cita_dt)
        inicio_intervalo = hora_actual - timedelta(minutes=30)
        fin_intervalo = hora_actual + timedelta(minutes=30)

        citas_en_dia = Cita_Veterinaria.objects.filter(fecha_cita=fecha_cita_dt)
        for cita in citas_en_dia:
            hora_existente = datetime.combine(cita.fecha_cita, cita.hora_cita)
            if inicio_intervalo <= hora_existente <= fin_intervalo:
                messages.error(request, "Debe haber al menos 30 minutos entre una cita y otra.")
                return redirect('crear')

        Cita_Veterinaria.objects.create(
            nombre_dueño=nombre_dueño,
            nombre_mascota=nombre_mascota,
            especie=especie,
            fecha_cita=fecha_cita,
            hora_cita=hora_cita,
            servicio=servicio,
            estatus_cita=estatus_cita,
            descripcion=descripcion
        )
        return redirect('listar')

    listar_servicio = Servicio.objects.all()
    contexto = {'servicio': listar_servicio}
    return render(request, 'crear.html', contexto)




@login_required
def editar_Cita_Veterinaria(request, id):
    cita_veterinaria = get_object_or_404(Cita_Veterinaria, id=id)
    listar_servicio = Servicio.objects.all()
    solo_estatus = request.user.has_perm('app.change_status_only')

    if request.method == 'POST':
        if solo_estatus:
            cita_veterinaria.estatus_cita = request.POST.get('estatus_cita', '').upper()
            cita_veterinaria.save()
            messages.success(request, "Estatus de la cita actualizado correctamente.")
            return redirect('listar')

        nombre_dueño = request.POST.get('nombre_dueño', '').upper()
        nombre_mascota = request.POST.get('nombre_mascota', '').upper()
        especie = request.POST.get('especie', '').upper()
        fecha_cita = request.POST.get('fecha_cita')
        hora_cita = request.POST.get('hora_cita')
        estatus_cita = request.POST.get('estatus_cita', '').upper()
        descripcion = request.POST.get('descripcion', '').upper()
        servicio_id = request.POST.get('servicio')

        # Validar formatos
        try:
            fecha_cita_dt = datetime.strptime(fecha_cita, "%Y-%m-%d").date()
            hora_cita_dt = datetime.strptime(hora_cita, "%H:%M").time()
        except (TypeError, ValueError):
            messages.error(request, "Formato de fecha u hora inválido.")
            return render(request, 'editar.html', {
                'cita_veterinaria': cita_veterinaria,
                'servicio': listar_servicio,
                'solo_estatus': solo_estatus
            })

        # Validar fecha anterior
        hoy = datetime.now().date()
        if fecha_cita_dt < hoy:
            messages.error(request, "No puedes establecer una cita en una fecha anterior a hoy.")
            return render(request, 'editar.html', {
                'cita_veterinaria': cita_veterinaria,
                'servicio': listar_servicio,
                'solo_estatus': solo_estatus
            })

        # Validar duplicados (otra cita con misma fecha y hora)
        if Cita_Veterinaria.objects.filter(
            fecha_cita=fecha_cita_dt, hora_cita=hora_cita_dt
        ).exclude(id=id).exists():
            messages.error(request, "Ya existe una cita en esa misma fecha y hora.")
            return render(request, 'editar.html', {
                'cita_veterinaria': cita_veterinaria,
                'servicio': listar_servicio,
                'solo_estatus': solo_estatus
            })

        # Validar lapso de 30 minutos
        hora_nueva = datetime.combine(fecha_cita_dt, hora_cita_dt)
        citas_en_dia = Cita_Veterinaria.objects.filter(fecha_cita=fecha_cita_dt).exclude(id=id)

        for cita in citas_en_dia:
            hora_existente = datetime.combine(cita.fecha_cita, cita.hora_cita)
            diferencia = abs((hora_nueva - hora_existente).total_seconds()) / 60
            if diferencia < 30:
                hora_conflicto = hora_existente.strftime("%I:%M %p")
                messages.error(request, f"No se puede registrar la cita. Hay otra programada a las {hora_conflicto}. Debe haber al menos 30 minutos de diferencia.")
                return render(request, 'editar.html', {
                    'cita_veterinaria': cita_veterinaria,
                    'servicio': listar_servicio,
                    'solo_estatus': solo_estatus
                })

        # Si todo está bien, guardar cambios
        cita_veterinaria.nombre_dueño = nombre_dueño
        cita_veterinaria.nombre_mascota = nombre_mascota
        cita_veterinaria.especie = especie
        cita_veterinaria.fecha_cita = fecha_cita
        cita_veterinaria.hora_cita = hora_cita
        cita_veterinaria.servicio = Servicio.objects.get(id=servicio_id)
        cita_veterinaria.estatus_cita = estatus_cita
        cita_veterinaria.descripcion = descripcion
        cita_veterinaria.save()

        messages.success(request, "Cita actualizada correctamente.")
        return redirect('listar')

    return render(request, 'editar.html', {
        'cita_veterinaria': cita_veterinaria,
        'servicio': listar_servicio,
        'solo_estatus': solo_estatus
    })



@permission_required('app.delete_citaveterinaria', raise_exception=True)
def eliminar_Cita_Veterinaria(request, id):
    cita = get_object_or_404(Cita_Veterinaria, id=id)
    cita.delete()
    return redirect('listar')

@permission_required('app.delete_citaveterinaria', raise_exception=True)
def crear_servicio(request):
    if request.method == 'POST':
        nombre = request.POST['nombre'].upper()
        descripcion = request.POST['descripcion'].upper()
        precio = request.POST['precio']

        Servicio.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio
        )
        return redirect('listar')  

    return render(request, 'crearservicio.html')