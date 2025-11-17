"""
PythonAnywhere WSGI konfiguratsiyasi - tuproqqala.pythonanywhere.com
Bu kodni /var/www/tuproqqala_pythonanywhere_com_wsgi.py fayliga qo'ying
"""

import os
import sys

# Project path - o'z path ingizga moslashtiring
# Agar loyiha /home/tuproqqala/Uztoziya da bo'lsa:
path = '/home/tuproqqala/Uztoziya'

# Agar loyiha /home/tuproqqala/mysite da bo'lsa, quyidagi qatorni ishlating:
# path = '/home/tuproqqala/mysite'

if path not in sys.path:
    sys.path.insert(0, path)

# Virtualenv path (agar kerak bo'lsa)
venv_path = os.path.join(path, 'venv')
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        with open(activate_this) as f:
            exec(f.read(), {'__file__': activate_this})

# Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

