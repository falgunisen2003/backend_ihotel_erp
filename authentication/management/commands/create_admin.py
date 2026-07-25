from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates default admin users for both default and hotel databases'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # 1. Create user in default DB
        try:
            u1, created1 = User.objects.using('default').get_or_create(
                username='admin', 
                defaults={'email': 'admin@example.com'}
            )
            u1.set_password('admin123')
            u1.is_superuser = True
            u1.is_staff = True
            u1.is_active = True
            u1.save(using='default')
            self.stdout.write(self.style.SUCCESS('Admin created in default database!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Default DB Error: {e}'))

        # 2. Create user in hotel DB
        try:
            u2, created2 = User.objects.using('hotel').get_or_create(
                username='admin', 
                defaults={'email': 'admin@example.com'}
            )
            u2.set_password('admin123')
            u2.is_superuser = True
            u2.is_staff = True
            u2.is_active = True
            u2.save(using='hotel')
            self.stdout.write(self.style.SUCCESS('Admin created in hotel database!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hotel DB Error: {e}'))

        self.stdout.write(self.style.SUCCESS('ADMIN CREATION PROCESS COMPLETED!'))