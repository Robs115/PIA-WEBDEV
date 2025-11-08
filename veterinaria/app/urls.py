from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('listar/', views.listar_Cita_Veterinaria, name='listar'),
    path('crear/', views.crear_Cita_Veterinaria, name='crear'),
    path('editar/<int:id>/', views.editar_Cita_Veterinaria, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_Cita_Veterinaria, name='eliminar'),
    path('crearservicio/', views.crear_servicio, name='crearservicio'),
]