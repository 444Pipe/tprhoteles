from django.contrib import admin
from .models import Municipio, Hotel, Reserva, Habitacion

class HabitacionInline(admin.TabularInline):
	model = Habitacion
	extra = 1
	fields = ('nombre', 'precio', 'capacidad', 'camas', 'metros_cuadrados', 'incluye_desayuno', 'estacionamiento', 'imagen_static', 'activa')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'tipo', 'municipio', 'direccion', 'imagen_static', 'tiene_mapa')
	search_fields = ('nombre', 'municipio__nombre')
	list_filter = ('municipio', 'tipo')
	inlines = [HabitacionInline]

	def tiene_mapa(self, obj):
		return bool(obj.mapa_embed_src)
	tiene_mapa.boolean = True
	tiene_mapa.short_description = 'Mapa'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
	list_display = ('hotel', 'nombre_cliente', 'email', 'fecha', 'personas', 'estado', 'creada')
	search_fields = ('nombre_cliente', 'hotel__nombre')
	list_filter = ('estado', 'hotel')


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'hotel', 'precio', 'capacidad', 'incluye_desayuno', 'estacionamiento', 'activa')
	search_fields = ('nombre', 'hotel__nombre')
	list_filter = ('hotel', 'activa', 'incluye_desayuno', 'estacionamiento')
