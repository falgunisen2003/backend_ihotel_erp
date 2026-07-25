from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates default admin users for both default and hotel databases'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create user in default DB
        u1, created1 = User.objects.using('default').get_or_create(
            username='admin', 
            defaults={'email': 'admin@example.com'}
        )
        u1.set_password('admin123')
        u1.is_superuser = True
        u1.is_staff = True
        u1.is_active = True
        u1.save()

        # Create user in hotel DB
        u2, created2 = User.objects.using('hotel').get_or_create(
            username='admin', 
            defaults={'email': 'admin@example.com'}
        )
        u2.set_password('admin123')
        u2.is_superuser = True
        u2.is_staff = True
        u2.is_active = True
        u2.save()

        self.stdout.write(self.style.SUCCESS('ADMIN USERS CREATED SUCCESSFULLY!'))