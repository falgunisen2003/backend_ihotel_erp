from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    if not User.objects.filter(username='admin').exists():
        user = User(
            username='admin',
            email='admin@example.com',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password('admin123')
        user.save()
    else:
        user = User.objects.get(username='admin')
        user.set_password('admin123')
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userhotel'),
    ]

    operations = [
        migrations.RunPython(create_admin, reverse_func),
    ]