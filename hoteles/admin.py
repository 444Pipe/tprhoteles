from django.contrib import admin
from .models import Municipio, Hotel, Reserva

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'tipo', 'municipio', 'direccion', 'imagen_static')
	search_fields = ('nombre', 'municipio__nombre')
	list_filter = ('municipio', 'tipo')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
	list_display = ('hotel', 'nombre_cliente', 'email', 'fecha', 'personas', 'estado', 'creada')
	search_fields = ('nombre_cliente', 'hotel__nombre')
	list_filter = ('estado', 'hotel')
