"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Auto-run migrations and load seed data on startup (for Render's ephemeral SQLite)
try:
    from django.core.management import call_command
    from django.db import connection
    
    # Always migrate to ensure tables exist
    print("Running migrations...")
    call_command('migrate', interactive=False)
    
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data.json')
    if os.path.exists(data_file):
        print("Loading initial data...")
        call_command('loaddata', data_file)
        print("Data loaded successfully.")
except Exception as e:
    print(f"Startup script error: {e}")

