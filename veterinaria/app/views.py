from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita_Veterinaria, Servicio
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages

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
        Cita_Veterinaria.objects.create(nombre_dueño=nombre_dueño, nombre_mascota=nombre_mascota, especie=especie, fecha_cita=fecha_cita, hora_cita=hora_cita, servicio=servicio, estatus_cita=estatus_cita, descripcion=descripcion)
        return redirect('listar')

    
    listar_servicio = Servicio.objects.all()
    contexto = {
        'servicio': listar_servicio
    }

    return render (request, 'crear.html', contexto)



@login_required
def editar_Cita_Veterinaria(request, id):
    cita_veterinaria = get_object_or_404(Cita_Veterinaria, id=id)

    solo_estatus = request.user.has_perm('app.change_status_only')

    if request.method == 'POST':
        if solo_estatus:
            cita_veterinaria.estatus_cita = request.POST['estatus_cita']
        else:
            cita_veterinaria.nombre_dueño = request.POST['nombre_dueño'].upper()
            cita_veterinaria.nombre_mascota = request.POST['nombre_mascota'].upper()
            cita_veterinaria.especie = request.POST['especie'].upper()
            cita_veterinaria.fecha_cita = request.POST['fecha_cita']
            cita_veterinaria.hora_cita = request.POST['hora_cita']
            cita_veterinaria.servicio = Servicio.objects.get(id=request.POST['servicio'])
            cita_veterinaria.estatus_cita = request.POST['estatus_cita'].upper()
            cita_veterinaria.descripcion = request.POST['descripcion'].upper()

        cita_veterinaria.save()
        return redirect('listar')
    
    listar_servicio = Servicio.objects.all()
    contexto = {
        'cita_veterinaria': cita_veterinaria,
        'servicio': listar_servicio,
        'solo_estatus': solo_estatus
    }
    
    return render (request, 'editar.html', contexto)


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