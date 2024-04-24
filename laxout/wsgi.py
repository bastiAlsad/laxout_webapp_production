"""
WSGI config for laxout project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laxout.settings')

path = '/home/dashboardlaxout/backup_laxout/laxout/server_tasks.py'
if path not in sys.path:
    sys.path.append(path)

application = get_wsgi_application()
