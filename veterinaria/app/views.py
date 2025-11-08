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
        
        estatus = request.POST['estatus']
        descripcion = request.POST['descripcion']
        motivo_id = request.POST['motivo']
        motivo = Servicio.objects.get(id=motivo_id)
        Cita_Veterinaria.objects.create(nombre_dueño=nombre_dueño, nombre_mascota=nombre_mascota, especie=especie, fecha_cita=fecha_cita, hora_cita=hora_cita, motivo=motivo, estatus=estatus, descripcion=descripcion)
        return redirect('listar')


    
    listar_servicio = Servicio.objects.all()
    contexto = {
        'servicio': listar_servicio
    }
    
    return render (request, 'crear.html', contexto)

@login_required
def editar_Cita_Veterinaria(request, id):
    Cita_Veterinaria = get_object_or_404(Cita_Veterinaria, id=id)
    if request.method == 'POST':
        Cita_Veterinaria.nombre_dueño = request.POST['nombre_dueño']
        Cita_Veterinaria.nombre_mascota = request.POST['nombre_mascota']
        Cita_Veterinaria.especie = request.POST['especie']
        Cita_Veterinaria.fecha_cita = request.POST['fecha_cita']
        Cita_Veterinaria.hora_cita = request.POST['hora_cita']
        Cita_Veterinaria.motivo = request.POST['motivo']
        Cita_Veterinaria.estatus = request.POST['estatus']
        Cita_Veterinaria.precio = request.POST['precio']
        Cita_Veterinaria.descripcion = request.POST['descripcion']
        Cita_Veterinaria.save()
        return redirect('listar')
    return render(request, 'editar.html', {'Cita_Veterinaria': Cita_Veterinaria})

@permission_required('app.delete_citaveterinaria', raise_exception=True)
def eliminar_Cita_Veterinaria(request, id):
    cita = get_object_or_404(Cita_Veterinaria, id=id)
    cita.delete()
    return redirect('listar')