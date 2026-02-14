from urllib.parse import quote
from datetime import timedelta

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone

from .models import Hotel, Municipio, Reserva


def _build_static_image_url(path):
	if not path:
		return ''
	cleaned = path.strip().replace('\\', '/').lstrip('/')
	if cleaned.startswith('static/'):
		cleaned = cleaned[len('static/'):]
	static_url = settings.STATIC_URL if settings.STATIC_URL.endswith('/') else f"{settings.STATIC_URL}/"
	return f"{static_url}{quote(cleaned, safe='/')}"


def _build_static_image_urls(raw_value):
	if not raw_value:
		return []
	parts = [part.strip() for part in str(raw_value).split(',') if part.strip()]
	return [_build_static_image_url(part) for part in parts]


def _attach_static_urls(hoteles):
	for hotel in hoteles:
		hotel.imagen_static_urls = _build_static_image_urls(hotel.imagen_static)
		hotel.imagen_static_url = hotel.imagen_static_urls[0] if hotel.imagen_static_urls else ''
	return hoteles


def hoteles_list(request):
	municipios = Municipio.objects.all()
	municipio_id = request.GET.get('municipio')
	hoteles = Hotel.objects.all()
	municipio_seleccionado = None
	if municipio_id:
		hoteles = hoteles.filter(municipio_id=municipio_id)
		municipio_seleccionado = int(municipio_id)
	hoteles = _attach_static_urls(hoteles)
	return render(request, 'hoteles_list.html', {
		'municipios': municipios,
		'hoteles': hoteles,
		'municipio_seleccionado': municipio_seleccionado
	})

class ReservaForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = ['fecha', 'fecha_salida', 'personas', 'habitaciones', 'nombre_cliente', 'email', 'telefono', 'observaciones']
		widgets = {
			'nombre_cliente': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Tu nombre',
			}),
			'email': forms.EmailInput(attrs={
				'class': 'form-control',
				'placeholder': 'tu@email.com',
			}),
			'telefono': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': '+57 3xx xxx xxxx',
			}),
			'fecha': forms.DateInput(attrs={
				'class': 'form-control',
				'type': 'date',
			}),
			'fecha_salida': forms.DateInput(attrs={
				'class': 'form-control',
				'type': 'date',
			}),
			'personas': forms.NumberInput(attrs={
				'class': 'form-control',
				'min': 1,
				'max': 20,
				'value': 2,
			}),
			'habitaciones': forms.NumberInput(attrs={
				'class': 'form-control',
				'min': 1,
				'max': 10,
				'value': 1,
			}),
			'observaciones': forms.Textarea(attrs={
				'class': 'form-control',
				'rows': 3,
				'placeholder': 'Preferencias de cama, hora de llegada, etc.',
			}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		hoy = timezone.localdate()
		self.fields['fecha'].widget.attrs['min'] = hoy.isoformat()
		self.fields['fecha_salida'].widget.attrs['min'] = (hoy + timedelta(days=1)).isoformat()

	def clean_fecha(self):
		fecha = self.cleaned_data.get('fecha')
		hoy = timezone.localdate()
		max_fecha = hoy + timedelta(days=365)
		if fecha and fecha < hoy:
			raise ValidationError('La fecha de reserva no puede ser anterior a hoy.')
		if fecha and fecha > max_fecha:
			raise ValidationError('La fecha de reserva no puede superar 1 año desde hoy.')
		return fecha

	def clean(self):
		cleaned_data = super().clean()
		fecha_entrada = cleaned_data.get('fecha')
		fecha_salida = cleaned_data.get('fecha_salida')
		if fecha_entrada and fecha_salida and fecha_salida <= fecha_entrada:
			self.add_error('fecha_salida', 'El check-out debe ser posterior al check-in.')
		return cleaned_data

	def clean_personas(self):
		personas = self.cleaned_data.get('personas')
		if personas is None or personas < 1:
			raise ValidationError('Debe reservar para al menos 1 persona.')
		if personas > 20:
			raise ValidationError('El máximo permitido por reserva es 20 personas.')
		return personas

	def clean_habitaciones(self):
		habitaciones = self.cleaned_data.get('habitaciones')
		if habitaciones is None or habitaciones < 1:
			raise ValidationError('Debe seleccionar al menos 1 habitación.')
		if habitaciones > 10:
			raise ValidationError('El máximo permitido por reserva es 10 habitaciones.')
		return habitaciones


class ReservaGeneralForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = ['hotel', 'fecha', 'fecha_salida', 'personas', 'habitaciones', 'nombre_cliente', 'email', 'telefono', 'observaciones']
		widgets = {
			'hotel': forms.Select(attrs={'class': 'form-select'}),
			'nombre_cliente': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Tu nombre',
			}),
			'email': forms.EmailInput(attrs={
				'class': 'form-control',
				'placeholder': 'tu@email.com',
			}),
			'telefono': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': '+57 3xx xxx xxxx',
			}),
			'fecha': forms.DateInput(attrs={
				'class': 'form-control',
				'type': 'date',
			}),
			'fecha_salida': forms.DateInput(attrs={
				'class': 'form-control',
				'type': 'date',
			}),
			'personas': forms.NumberInput(attrs={
				'class': 'form-control',
				'min': 1,
				'max': 20,
				'value': 2,
			}),
			'habitaciones': forms.NumberInput(attrs={
				'class': 'form-control',
				'min': 1,
				'max': 10,
				'value': 1,
			}),
			'observaciones': forms.Textarea(attrs={
				'class': 'form-control',
				'rows': 3,
				'placeholder': 'Preferencias de cama, hora de llegada, etc.',
			}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['hotel'].queryset = Hotel.objects.all().order_by('nombre')
		hoy = timezone.localdate()
		self.fields['fecha'].widget.attrs['min'] = hoy.isoformat()
		self.fields['fecha_salida'].widget.attrs['min'] = (hoy + timedelta(days=1)).isoformat()

	def clean_fecha(self):
		fecha = self.cleaned_data.get('fecha')
		hoy = timezone.localdate()
		max_fecha = hoy + timedelta(days=365)
		if fecha and fecha < hoy:
			raise ValidationError('La fecha de reserva no puede ser anterior a hoy.')
		if fecha and fecha > max_fecha:
			raise ValidationError('La fecha de reserva no puede superar 1 año desde hoy.')
		return fecha

	def clean(self):
		cleaned_data = super().clean()
		fecha_entrada = cleaned_data.get('fecha')
		fecha_salida = cleaned_data.get('fecha_salida')
		if fecha_entrada and fecha_salida and fecha_salida <= fecha_entrada:
			self.add_error('fecha_salida', 'El check-out debe ser posterior al check-in.')
		return cleaned_data

	def clean_personas(self):
		personas = self.cleaned_data.get('personas')
		if personas is None or personas < 1:
			raise ValidationError('Debe reservar para al menos 1 persona.')
		if personas > 20:
			raise ValidationError('El máximo permitido por reserva es 20 personas.')
		return personas

	def clean_habitaciones(self):
		habitaciones = self.cleaned_data.get('habitaciones')
		if habitaciones is None or habitaciones < 1:
			raise ValidationError('Debe seleccionar al menos 1 habitación.')
		if habitaciones > 10:
			raise ValidationError('El máximo permitido por reserva es 10 habitaciones.')
		return habitaciones

def index(request):
	municipios = Municipio.objects.all()
	municipio_id = request.GET.get('municipio')
	hoteles = Hotel.objects.all()
	municipio_seleccionado = None
	if municipio_id:
		hoteles = hoteles.filter(municipio_id=municipio_id)
		municipio_seleccionado = int(municipio_id)
	hoteles = _attach_static_urls(hoteles)
	return render(request, 'index.html', {
		'municipios': municipios,
		'hoteles': hoteles,
		'municipio_seleccionado': municipio_seleccionado
	})

def hotel_detail(request, hotel_id):
	hotel = get_object_or_404(Hotel, id=hotel_id)
	hotel.imagen_static_urls = _build_static_image_urls(hotel.imagen_static)
	hotel.imagen_static_url = hotel.imagen_static_urls[0] if hotel.imagen_static_urls else ''
	habitaciones = list(hotel.habitaciones.filter(activa=True))
	galeria_imagenes = []
	if hotel.imagen_static_urls:
		galeria_imagenes.extend(hotel.imagen_static_urls)
	elif hotel.imagen_static_url:
		galeria_imagenes.append(hotel.imagen_static_url)
	elif hotel.imagen:
		galeria_imagenes.append(hotel.imagen.url)

	for habitacion in habitaciones:
		habitacion.imagen_static_urls = _build_static_image_urls(habitacion.imagen_static)
		habitacion.imagen_static_url = habitacion.imagen_static_urls[0] if habitacion.imagen_static_urls else ''
		if habitacion.imagen_static_urls:
			galeria_imagenes.extend(habitacion.imagen_static_urls)
		elif habitacion.imagen_static_url:
			galeria_imagenes.append(habitacion.imagen_static_url)

	# Deduplicar galería conservando orden
	galeria_imagenes = list(dict.fromkeys(galeria_imagenes))

	precio_desde = None
	if habitaciones:
		precio_desde = min(habitacion.precio for habitacion in habitaciones)

	context = {
		'hotel': hotel,
		'habitaciones': habitaciones,
		'galeria_imagenes': galeria_imagenes,
		'total_habitaciones': len(habitaciones),
		'precio_desde': precio_desde,
	}
	return render(request, 'hotel_detail.html', context)

def reservar(request, hotel_id):
	hotel = get_object_or_404(Hotel, id=hotel_id)
	if request.method == 'POST':
		form = ReservaForm(request.POST)
		if form.is_valid():
			reserva = form.save(commit=False)
			reserva.hotel = hotel
			reserva.save()
			return render(request, 'reserva_exitosa.html', {'hotel': hotel, 'reserva': reserva})
	else:
		form = ReservaForm()
	return render(request, 'reservar.html', {'hotel': hotel, 'form': form})


def reservar_general(request):
	hoteles_disponibles = Hotel.objects.select_related('municipio').all().order_by('nombre')
	if request.method == 'POST':
		form = ReservaGeneralForm(request.POST)
		if form.is_valid():
			reserva = form.save()
			return render(request, 'reserva_exitosa.html', {'hotel': reserva.hotel, 'reserva': reserva})
	else:
		form = ReservaGeneralForm()
	return render(request, 'reservar.html', {'hotel': None, 'form': form, 'hoteles_disponibles': hoteles_disponibles})


def logout_view(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente.')
	return redirect('index')


def admin_logout_redirect(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente.')
	return redirect('index')
