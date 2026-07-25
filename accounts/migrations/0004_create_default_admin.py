from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    hashed_password = make_password('admin123')

    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@example.com',
            password=hashed_password,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
    else:
        User.objects.filter(username='admin').update(
            password=hashed_password,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userhotel'),
    ]

    operations = [
        migrations.RunPython(create_admin, reverse_func),
    ]