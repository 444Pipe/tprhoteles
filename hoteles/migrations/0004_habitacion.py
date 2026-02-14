from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0003_hotel_ubicacion_mapa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capacidad', models.PositiveIntegerField(default=2)),
                ('camas', models.CharField(blank=True, default='', max_length=120)),
                ('metros_cuadrados', models.PositiveIntegerField(blank=True, null=True)),
                ('incluye_desayuno', models.BooleanField(default=False)),
                ('estacionamiento', models.BooleanField(default=False)),
                ('imagen_static', models.CharField(blank=True, default='', max_length=255)),
                ('activa', models.BooleanField(default=True)),
                ('hotel', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='habitaciones', to='hoteles.hotel')),
            ],
            options={
                'ordering': ['precio', 'nombre'],
            },
        ),
    ]
