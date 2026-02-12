

from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Municipio, Reserva
from django import forms

class ReservaForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = ['nombre_cliente', 'email', 'fecha', 'personas']

def index(request):
	municipios = Municipio.objects.all()
	municipio_id = request.GET.get('municipio')
	hoteles = Hotel.objects.all()
	municipio_seleccionado = None
	if municipio_id:
		hoteles = hoteles.filter(municipio_id=municipio_id)
		municipio_seleccionado = int(municipio_id)
	return render(request, 'index.html', {
		'municipios': municipios,
		'hoteles': hoteles,
		'municipio_seleccionado': municipio_seleccionado
	})

def hotel_detail(request, hotel_id):
	hotel = get_object_or_404(Hotel, id=hotel_id)
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
