from django.core.management.base import BaseCommand

from hoteles.models import Hotel, Municipio


SEED_DATA = {
    "Castilla La Nueva": [
        {
            "nombre": "Hotel Boutique - TPR Castilla",
            "tipo": "Hotel Boutique",
            "direccion": "Castilla La Nueva, Meta",
            "descripcion": "Hotel boutique con ambiente tranquilo, habitaciones confortables y servicio personalizado para viajes de descanso o trabajo.",
            "imagen_static": "Hotel Boutique  - TPR Castilla.jpeg",
        },
    ],
    "Acacías": [
        {
            "nombre": "Hotel Boutique - Tierra Bendecida",
            "tipo": "Hotel Boutique",
            "direccion": "Acacías, Meta",
            "descripcion": "Espacio acogedor con diseño moderno, ideal para descansar y disfrutar de la cultura llanera en una ubicación estratégica.",
            "imagen_static": "Hotel Boutique  - Tierra Bendecida.jpeg",
        },
    ],
    "Villavicencio": [
        {
            "nombre": "Hotel Boutique - Los Reyes",
            "tipo": "Hotel Boutique",
            "direccion": "Villavicencio, Meta",
            "descripcion": "Hotel elegante en zona urbana con excelente conectividad, perfecto para turismo, eventos y viajes corporativos.",
            "imagen_static": "Hotel Boutique  - Los Reyes.jpeg",
        },
        {
            "nombre": "Aparta Hotel - Maydu",
            "tipo": "Aparta Hotel",
            "direccion": "Villavicencio, Meta",
            "descripcion": "Aparta hotel funcional para estancias cortas o largas, con comodidad, independencia y ubicación conveniente.",
            "imagen_static": "Aparta Hotel - Maydu.jpeg",
        },
    ],
}


class Command(BaseCommand):
    help = "Carga municipios y hoteles iniciales para el proyecto"

    def handle(self, *args, **options):
        municipios_creados = 0
        hoteles_creados = 0
        hoteles_actualizados = 0

        for municipio_nombre, hoteles in SEED_DATA.items():
            municipio, created = Municipio.objects.get_or_create(nombre=municipio_nombre)
            if created:
                municipios_creados += 1

            for hotel_data in hoteles:
                hotel, hotel_created = Hotel.objects.get_or_create(
                    nombre=hotel_data["nombre"],
                    defaults={
                        "tipo": hotel_data["tipo"],
                        "municipio": municipio,
                        "direccion": hotel_data["direccion"],
                        "descripcion": hotel_data["descripcion"],
                        "imagen_static": hotel_data.get("imagen_static", ""),
                    },
                )
                if hotel_created:
                    hoteles_creados += 1
                else:
                    updated_fields = []
                    if hotel.tipo != hotel_data["tipo"]:
                        hotel.tipo = hotel_data["tipo"]
                        updated_fields.append("tipo")
                    if hotel.municipio_id != municipio.id:
                        hotel.municipio = municipio
                        updated_fields.append("municipio")
                    if hotel.direccion != hotel_data["direccion"]:
                        hotel.direccion = hotel_data["direccion"]
                        updated_fields.append("direccion")
                    if hotel.descripcion != hotel_data["descripcion"]:
                        hotel.descripcion = hotel_data["descripcion"]
                        updated_fields.append("descripcion")
                    if hotel.imagen_static != hotel_data.get("imagen_static", ""):
                        hotel.imagen_static = hotel_data.get("imagen_static", "")
                        updated_fields.append("imagen_static")
                    if updated_fields:
                        hotel.save(update_fields=updated_fields)
                        hoteles_actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completado: {municipios_creados} municipios nuevos, {hoteles_creados} hoteles nuevos, {hoteles_actualizados} hoteles actualizados."
            )
        )
