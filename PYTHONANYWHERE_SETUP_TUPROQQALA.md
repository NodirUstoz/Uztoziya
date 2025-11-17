# PythonAnywhere Sozlash - tuproqqala.pythonanywhere.com

## 📋 Sizning Ma'lumotlaringiz

- **Username**: tuproqqala
- **Domain**: tuproqqala.pythonanywhere.com
- **Python Version**: 3.11
- **WSGI File**: /var/www/tuproqqala_pythonanywhere_com_wsgi.py
- **Source Code**: /home/tuproqqala/Uztoziya (yoki /home/tuproqqala/mysite)

## 🔧 Sozlash Qadamlar

### 1. Source Code Path ni Tekshiring

Bash console da:

```bash
cd ~
ls -la
```

Agar loyiha `/home/tuproqqala/Uztoziya` da bo'lsa - yaxshi!
Agar `/home/tuproqqala/mysite` da bo'lsa, uni `/home/tuproqqala/Uztoziya` ga ko'chiring yoki WSGI da path ni o'zgartiring.

### 2. Virtual Environment Yaratish (Agar hali yaratilmagan bo'lsa)

```bash
cd ~/Uztoziya  # yoki ~/mysite
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables (.env fayl)

```bash
cd ~/Uztoziya  # yoki ~/mysite
nano .env
```

Quyidagi ma'lumotlarni kiriting:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=tuproqqala.pythonanywhere.com
DATABASE_URL=
CORS_ALLOW_ALL_ORIGINS=False
TESSERACT_PATH=/usr/bin/tesseract

# API Keys (agar kerak bo'lsa)
OPENAI_API_KEY=your-openai-key
GOOGLE_GEMINI_API_KEY=your-gemini-key
GOOGLE_API_KEY=your-google-api-key
```

**Eslatma**: Secret key yaratish:
```bash
python3.11 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Database Migration

```bash
cd ~/Uztoziya  # yoki ~/mysite
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 5. Web App Sozlamalari

#### A) Source Code Path

Dashboard > Web > "Source code" bo'limida:
- Agar loyiha `/home/tuproqqala/Uztoziya` da bo'lsa: `/home/tuproqqala/Uztoziya`
- Agar `/home/tuproqqala/mysite` da bo'lsa: `/home/tuproqqala/mysite`

#### B) Working Directory

Dashboard > Web > "Working directory":
- `/home/tuproqqala/` yoki `/home/tuproqqala/Uztoziya`

#### C) Virtualenv

Dashboard > Web > "Virtualenv" bo'limida:
```
/home/tuproqqala/Uztoziya/venv
```
yoki agar `mysite` da bo'lsa:
```
/home/tuproqqala/mysite/venv
```

#### D) WSGI Configuration

Dashboard > Web > "WSGI configuration file" linkini bosing va quyidagi kodni qo'ying:

**Agar loyiha `/home/tuproqqala/Uztoziya` da bo'lsa:**

```python
import os
import sys

# Project path
path = '/home/tuproqqala/Uztoziya'
if path not in sys.path:
    sys.path.insert(0, path)

# Virtualenv path (agar kerak bo'lsa)
venv_path = '/home/tuproqqala/Uztoziya/venv'
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        with open(activate_this) as f:
            exec(f.read(), {'__file__': activate_this})

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Agar loyiha `/home/tuproqqala/mysite` da bo'lsa:**

```python
import os
import sys

# Project path
path = '/home/tuproqqala/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Virtualenv path (agar kerak bo'lsa)
venv_path = '/home/tuproqqala/mysite/venv'
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        with open(activate_this) as f:
            exec(f.read(), {'__file__': activate_this})

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### E) Static Files

Dashboard > Web > "Static files" bo'limida quyidagilarni qo'shing:

**Agar loyiha `/home/tuproqqala/Uztoziya` da bo'lsa:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuproqqala/Uztoziya/staticfiles` |
| `/media/` | `/home/tuproqqala/Uztoziya/media` |

**Agar loyiha `/home/tuproqqala/mysite` da bo'lsa:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuproqqala/mysite/staticfiles` |
| `/media/` | `/home/tuproqqala/mysite/media` |

### 6. Reload Web App

Dashboard > Web > "Reload" tugmasini bosing va bir necha soniya kuting.

### 7. Tekshirish

Brauzerda oching: `https://tuproqqala.pythonanywhere.com`

## 🐛 Muammolarni Hal Qilish

### Error Log ni Tekshiring

Dashboard > Web > "Error log" ni ochib, xatolarni ko'ring.

### Import Error

Agar "Module not found" xatosi bo'lsa:

1. Virtualenv to'g'ri sozlanganligini tekshiring
2. WSGI da path to'g'ri ekanligini tekshiring
3. Barcha paketlar o'rnatilganligini tekshiring:

```bash
cd ~/Uztoziya  # yoki ~/mysite
source venv/bin/activate
pip install -r requirements.txt
```

### Static Files Ko'rinmayapti

1. `collectstatic` bajarilganligini tekshiring
2. Static files path to'g'ri ekanligini tekshiring
3. Reload qiling

### Database Error

1. `.env` fayl to'g'ri sozlanganligini tekshiring
2. Migration bajarilganligini tekshiring:

```bash
cd ~/Uztoziya  # yoki ~/mysite
source venv/bin/activate
python manage.py migrate
```

## ✅ Tekshirish Ro'yxati

- [ ] Source code path to'g'ri
- [ ] Virtualenv yaratilgan va paketlar o'rnatilgan
- [ ] `.env` fayl yaratilgan va to'g'ri sozlangan
- [ ] Database migration bajarilgan
- [ ] Superuser yaratilgan
- [ ] Static files yig'ilgan (`collectstatic`)
- [ ] WSGI configuration to'g'ri sozlangan
- [ ] Virtualenv path to'g'ri ko'rsatilgan
- [ ] Static files paths to'g'ri sozlangan
- [ ] Web app reload qilingan
- [ ] Sayt ishlayapti

---

**Muvaffaqiyat! 🚀**

