from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita_Veterinaria, Servicio
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    citas = Cita_Veterinaria.objects.all()
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

@login_required
def listar_Cita_Veterinaria(request):
    citas = Cita_Veterinaria.objects.all()
    return render(request, 'listar.html', {'citas': citas})

@login_required
def crear_Cita_Veterinaria(request):
    if request.method == 'POST':
        nombre_dueño = request.POST['nombre_dueño']
        nombre_mascota = request.POST['nombre_mascota']
        especie = request.POST['especie']
        fecha_cita = request.POST['fecha_cita']
        hora_cita = request.POST['hora_cita']
        
        estatus_cita = request.POST['estatus_cita']
        descripcion = request.POST['descripcion']
        servicio_id = request.POST['servicio']
        servicio = Servicio.objects.get(id=servicio_id)
        Cita_Veterinaria.objects.create(nombre_dueño=nombre_dueño, nombre_mascota=nombre_mascota, especie=especie, fecha_cita=fecha_cita, hora_cita=hora_cita, servicio=servicio, estatus_cita=estatus_cita, descripcion=descripcion)
        return redirect('listar')


    
    listar_servicio = Servicio.objects.all()
    contexto = {
        'servicio': listar_servicio
    }
    
    return render (request, 'crer.html', contexto)

@login_required
def editar_Cita_Veterinaria(request, id):
    cita_veterinaria = get_object_or_404(Cita_Veterinaria, id=id)
    if request.method == 'POST':
        cita_veterinaria.nombre_dueño = request.POST['nombre_dueño']
        cita_veterinaria.nombre_mascota = request.POST['nombre_mascota']
        cita_veterinaria.especie = request.POST['especie']
        cita_veterinaria.fecha_cita = request.POST['fecha_cita']
        cita_veterinaria.hora_cita = request.POST['hora_cita']
        cita_veterinaria.servicio = Servicio.objects.get(id=request.POST['servicio'])
        cita_veterinaria.estatus_cita = request.POST['estatus_cita']
        cita_veterinaria.descripcion = request.POST['descripcion']
        cita_veterinaria.save()
        return redirect('listar')
    
    listar_servicio = Servicio.objects.all()
    contexto = {
        'cita_veterinaria': cita_veterinaria,
        'servicio': listar_servicio
    }
    
    return render (request, 'editar.html', contexto)


@permission_required('app.delete_citaveterinaria', raise_exception=True)
def eliminar_Cita_Veterinaria(request, id):
    cita = get_object_or_404(Cita_Veterinaria, id=id)
    cita.delete()
    return redirect('listar')