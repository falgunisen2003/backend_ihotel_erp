from django.db import migrations


def create_hotel_and_role(apps, schema_editor):
    HotelGroup = apps.get_model('hotels', 'HotelGroup')
    Hotel = apps.get_model('hotels', 'Hotel')
    Role = apps.get_model('roles', 'Role')
    User = apps.get_model('accounts', 'User')
    UserHotel = apps.get_model('accounts', 'UserHotel')

    group, _ = HotelGroup.objects.get_or_create(
        code='DEFAULT',
        defaults={'name': 'Default Hotel Group', 'is_active': True}
    )

    hotel, _ = Hotel.objects.get_or_create(
        code='DEFAULT',
        defaults={
            'group': group,
            'name': 'Default Hotel',
            'database_name': 'default_hotel_db',
            'database_user': 'default_hotel_user',
            'database_password': 'changeme123',
            'is_active': True,
        }
    )

    role, _ = Role.objects.get_or_create(
        name='Super Admin',
        defaults={'description': 'Full system access', 'is_active': True}
    )

    admin_user = User.objects.filter(username='admin').first()

    if admin_user:
        UserHotel.objects.get_or_create(
            user=admin_user,
            hotel=hotel,
            defaults={
                'role': role,
                'is_default': True,
                'is_active': True,
            }
        )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_create_default_admin'),
        ('hotels', '0005_alter_hotel_city_alter_hotel_country_and_more'),
        ('roles', '0002_rolepermission'),
    ]

    operations = [
        migrations.RunPython(create_hotel_and_role, reverse_func),
    ]