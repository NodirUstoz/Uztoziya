"""
PythonAnywhere uchun WSGI konfiguratsiyasi
Bu faylni PythonAnywhere Dashboard > Web > WSGI configuration file ga qo'ying
"""

import os
import sys

# PythonAnywhere da project path ni o'rnating
# Masalan: /home/yourusername/Uztoziya
path = '/home/yourusername/Uztoziya'  # O'z username ingizni qo'ying
if path not in sys.path:
    sys.path.insert(0, path)

# Django settings module ni o'rnating
os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

# Django WSGI application ni import qiling
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

