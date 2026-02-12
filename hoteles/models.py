
from django.db import models

class Municipio(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre


class Hotel(models.Model):
	nombre = models.CharField(max_length=100)
	tipo = models.CharField(max_length=50)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
	direccion = models.CharField(max_length=200)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='hoteles/', blank=True, null=True)

	def __str__(self):
		return self.nombre


class Reserva(models.Model):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	nombre_cliente = models.CharField(max_length=100)
	email = models.EmailField()
	fecha = models.DateField()
	personas = models.PositiveIntegerField()
	estado = models.CharField(max_length=20, default='Pendiente')
	creada = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Reserva de {self.nombre_cliente} en {self.hotel.nombre}"
