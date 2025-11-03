from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita_Veterinaria, Servicio

def index(request):
    citas = Cita_Veterinaria.objects.all()
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def listar_Cita_Veterinaria(request):
    citas = Cita_Veterinaria.objects.all()
    return render(request, 'listar.html', {'citas': citas})

def crear_Cita_Veterinaria(request):
    if request.method == 'POST':
        nombre_dueño = request.POST['nombre_dueño']
        nombre_mascota = request.POST['nombre_mascota']
        especie = request.POST['especie']
        fecha_cita = request.POST['fecha_cita']
        hora_cita = request.POST['hora_cita']
        motivo = request.POST['motivo']
        estatus = request.POST['estatus']
        descripcion = request.POST['descripcion']
        Cita_Veterinaria.objects.create(nombre_dueño=nombre_dueño, nombre_mascota=nombre_mascota, especie=especie, fecha_cita=fecha_cita, hora_cita=hora_cita, motivo=motivo, estatus=estatus, descripcion=descripcion)
        return redirect('listar')
    return render(request, 'crear.html')

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

def eliminar_Cita_Veterinaria(request, id):
    Cita_Veterinaria = get_object_or_404(Cita_Veterinaria, id=id)
    Cita_Veterinaria.delete()
    return redirect('listar')