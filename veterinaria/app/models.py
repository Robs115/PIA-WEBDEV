from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class Cita_Veterinaria(models.Model):
    nombre_dueño = models.CharField(max_length=100)
    nombre_mascota = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    
    estatus_cita = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True)


    def __str__(self):
        return self.nombre_dueño
    
    class Meta:
        permissions = [
            ("consulta_full_edit", "Puede cambiar todos los elementos de una cita."),
        ]
