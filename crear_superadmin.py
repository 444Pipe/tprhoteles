import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadena_hoteles.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciales configurables por variables de entorno
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@tprhoteles.com')
password = os.environ.get('ADMIN_PASSWORD', 'admin1234')

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    },
)

if created:
    user.set_password(password)
    user.save(update_fields=['password'])
    print('Superusuario creado')
else:
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save(update_fields=['email', 'is_staff', 'is_superuser', 'is_active', 'password'])
    print('Superusuario actualizado y contraseña restablecida')
