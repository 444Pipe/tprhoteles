import re

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
	imagen_static = models.CharField(max_length=255, blank=True, default='')
	imagen = models.ImageField(upload_to='hoteles/', blank=True, null=True)
	ubicacion_mapa = models.TextField(blank=True, default='')

	@property
	def mapa_embed_src(self):
		value = (self.ubicacion_mapa or '').strip()
		if not value:
			return ''

		match = re.search(r'''src=["']([^"']+)["']''', value)
		if match:
			return match.group(1)

		if value.startswith('http://') or value.startswith('https://'):
			return value

		return ''

	def __str__(self):
		return self.nombre


class Habitacion(models.Model):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')
	nombre = models.CharField(max_length=120)
	descripcion = models.TextField(blank=True, default='')
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	capacidad = models.PositiveIntegerField(default=2)
	camas = models.CharField(max_length=120, blank=True, default='')
	metros_cuadrados = models.PositiveIntegerField(blank=True, null=True)
	incluye_desayuno = models.BooleanField(default=False)
	estacionamiento = models.BooleanField(default=False)
	imagen_static = models.CharField(max_length=255, blank=True, default='')
	activa = models.BooleanField(default=True)

	class Meta:
		ordering = ['precio', 'nombre']

	def __str__(self):
		return f"{self.nombre} - {self.hotel.nombre}"


class Reserva(models.Model):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	nombre_cliente = models.CharField(max_length=100)
	email = models.EmailField()
	fecha = models.DateField()
	fecha_salida = models.DateField(blank=True, null=True)
	personas = models.PositiveIntegerField()
	habitaciones = models.PositiveIntegerField(default=1)
	telefono = models.CharField(max_length=30, blank=True, default='')
	observaciones = models.TextField(blank=True, default='')
	estado = models.CharField(max_length=20, default='Pendiente')
	creada = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Reserva de {self.nombre_cliente} en {self.hotel.nombre}"
