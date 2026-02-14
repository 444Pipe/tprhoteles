from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0004_habitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='habitaciones',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='reserva',
            name='observaciones',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='reserva',
            name='telefono',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
