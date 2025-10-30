from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listar/', views.listar_Cita_Veterinaria, name='listar'),
    path('crear/', views.crear_Cita_Veterinaria, name='crear'),
    path('editar/<int:id>/', views.editar_Cita_Veterinaria, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_Cita_Veterinaria, name='eliminar'),
]