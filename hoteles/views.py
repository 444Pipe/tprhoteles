from urllib.parse import quote

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth import logout
from django.contrib import messages

from .models import Hotel, Municipio, Reserva


def _build_static_image_url(path):
	if not path:
		return ''
	cleaned = path.strip().replace('\\', '/').lstrip('/')
	if cleaned.startswith('static/'):
		cleaned = cleaned[len('static/'):]
	static_url = settings.STATIC_URL if settings.STATIC_URL.endswith('/') else f"{settings.STATIC_URL}/"
	return f"{static_url}{quote(cleaned, safe='/')}"


def _attach_static_urls(hoteles):
	for hotel in hoteles:
		hotel.imagen_static_url = _build_static_image_url(hotel.imagen_static)
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
		fields = ['nombre_cliente', 'email', 'fecha', 'personas']


class ReservaGeneralForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = ['hotel', 'nombre_cliente', 'email', 'fecha', 'personas']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['hotel'].queryset = Hotel.objects.all().order_by('nombre')

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
	hotel.imagen_static_url = _build_static_image_url(hotel.imagen_static)
	return render(request, 'hotel_detail.html', {'hotel': hotel})

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
	if request.method == 'POST':
		form = ReservaGeneralForm(request.POST)
		if form.is_valid():
			reserva = form.save()
			return render(request, 'reserva_exitosa.html', {'hotel': reserva.hotel, 'reserva': reserva})
	else:
		form = ReservaGeneralForm()
	return render(request, 'reservar.html', {'hotel': None, 'form': form})


def logout_view(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente.')
	return redirect('index')


def admin_logout_redirect(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente.')
	return redirect('index')
