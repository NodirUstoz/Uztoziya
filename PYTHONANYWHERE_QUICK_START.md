# PythonAnywhere - Tezkor Boshlash

## 1. Loyihani Yuklash

```bash
cd ~
git clone https://github.com/yourusername/Uztoziya.git
cd Uztoziya
```

## 2. Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Environment Variables

`.env` fayl yarating:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
TESSERACT_PATH=/usr/bin/tesseract
```

## 4. Database Migration

```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 5. Web App Sozlash

1. Dashboard > "Web" > "Add a new web app"
2. "Manual configuration" tanlang
3. Python 3.10 yoki 3.11 tanlang

## 6. WSGI Configuration

WSGI faylga quyidagini qo'ying:

```python
import os
import sys

path = '/home/yourusername/Uztoziya'  # O'z username ingizni qo'ying
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 7. Static Files

Web tab > Static files:

- `/static/` → `/home/yourusername/Uztoziya/staticfiles`
- `/media/` → `/home/yourusername/Uztoziya/media`

## 8. Reload

Web tab > "Reload" tugmasini bosing.

## ✅ Tayyor!

Sizning domain: `https://yourusername.pythonanywhere.com`

Batafsil qo'llanma: `PYTHONANYWHERE_DEPLOYMENT.md`

