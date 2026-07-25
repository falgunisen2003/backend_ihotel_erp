import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from django.conf import settings
from .models import Hotel

@receiver(post_save, sender=Hotel)
def create_tenant_database(sender, instance, created, **kwargs):
    if created and instance.db_name:
        db_name = instance.db_name
        
        # 1. Connect to PostgreSQL master engine to create new database
        db_settings = settings.DATABASES['default']
        try:
            con = psycopg2.connect(
                dbname='postgres',
                user=db_settings['USER'],
                password=db_settings['PASSWORD'],
                host=db_settings['HOST'],
                port=db_settings['PORT']
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = con.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}";')
            cursor.close()
            con.close()
            print(f"✅ Database '{db_name}' created successfully on PostgreSQL.")
        except Exception as e:
            print(f"⚠️ Database creation note: {e}")

        # 2. Update dynamic connection settings & run tenant migrations
        settings.DATABASES['hotel']['NAME'] = db_name
        try:
            call_command('migrate', database='hotel')
            print(f"✅ Tenant migrations applied to '{db_name}' successfully.")
        except Exception as e:
            print(f"❌ Migration failed for '{db_name}': {e}")