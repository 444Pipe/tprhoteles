from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0002_hotel_imagen_static'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='ubicacion_mapa',
            field=models.TextField(blank=True, default=''),
        ),
    ]
