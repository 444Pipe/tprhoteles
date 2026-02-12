import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadena_hoteles.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Cambia estos valores por los que desees
username = 'admin'
email = 'delgadofelipe315@gmail.com'
password = 'admin1234'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superusuario creado')
else:
    print('El superusuario ya existe')
