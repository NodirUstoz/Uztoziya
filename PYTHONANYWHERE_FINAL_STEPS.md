# PythonAnywhere - Yakuniy Sozlash Qadamlar

## ✅ Hozirgi Holat

- ✅ Loyiha yuklangan: `/home/tuproqqala/Uztoziya`
- ✅ Virtualenv mavjud: `/home/tuproqqala/Uztoziya/venv`
- ✅ Barcha fayllar mavjud

## 🔧 Keyingi Qadamlar

### 1. .env Fayl Yaratish

Bash console da:

```bash
cd ~/Uztoziya
nano .env
```

Quyidagi ma'lumotlarni kiriting (Ctrl+X, Y, Enter bilan saqlang):

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=tuproqqala.pythonanywhere.com
DATABASE_URL=
CORS_ALLOW_ALL_ORIGINS=False
TESSERACT_PATH=/usr/bin/tesseract

# API Keys (agar kerak bo'lsa)
OPENAI_API_KEY=
GOOGLE_GEMINI_API_KEY=
GOOGLE_API_KEY=
```

**Secret Key yaratish:**
```bash
cd ~/Uztoziya
source venv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Bu key ni `.env` faylga qo'ying.

### 2. Paketlarni O'rnatish (Agar hali o'rnatilmagan bo'lsa)

```bash
cd ~/Uztoziya
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Database Migration

```bash
cd ~/Uztoziya
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4. Web App Sozlamalari

Dashboard > Web tab ga kiring va quyidagilarni sozlang:

#### A) Source Code
```
/home/tuproqqala/Uztoziya
```

#### B) Working Directory
```
/home/tuproqqala/Uztoziya
```

#### C) Virtualenv
```
/home/tuproqqala/Uztoziya/venv
```

#### D) WSGI Configuration

"WSGI configuration file" linkini bosing va **BARCHA MAVJUD KODNI O'CHIRIB**, quyidagini qo'ying:

```python
import os
import sys

# Project path
path = '/home/tuproqqala/Uztoziya'
if path not in sys.path:
    sys.path.insert(0, path)

# Virtualenv activation
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

**"Save" tugmasini bosing!**

#### E) Static Files

"Static files" bo'limida quyidagilarni qo'shing:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuproqqala/Uztoziya/staticfiles` |
| `/media/` | `/home/tuproqqala/Uztoziya/media` |

**"Add" tugmasini bosing har biriga!**

### 5. Reload Web App

Dashboard > Web > **"Reload"** tugmasini bosing va 10-15 soniya kuting.

### 6. Tekshirish

Brauzerda oching: **https://tuproqqala.pythonanywhere.com**

## 🐛 Agar Xatolik Bo'lsa

### Error Log ni Tekshiring

Dashboard > Web > "Error log" ni ochib, xatolarni ko'ring.

### Eng Keng Tarqalgan Xatolar:

1. **ImportError: No module named 'django'**
   - Virtualenv to'g'ri sozlanganligini tekshiring
   - Paketlar o'rnatilganligini tekshiring: `pip install -r requirements.txt`

2. **ModuleNotFoundError: No module named 'ustoziya_platform'**
   - WSGI da path to'g'ri ekanligini tekshiring
   - Source code path to'g'ri ekanligini tekshiring

3. **DisallowedHost**
   - `.env` faylda `ALLOWED_HOSTS=tuproqqala.pythonanywhere.com` ekanligini tekshiring

4. **Static files ko'rinmayapti**
   - `collectstatic` bajarilganligini tekshiring
   - Static files paths to'g'ri ekanligini tekshiring

## ✅ Tekshirish Ro'yxati

- [ ] `.env` fayl yaratilgan va to'g'ri sozlangan
- [ ] Barcha paketlar o'rnatilgan
- [ ] Database migration bajarilgan
- [ ] Superuser yaratilgan
- [ ] Static files yig'ilgan
- [ ] WSGI configuration to'g'ri sozlangan
- [ ] Virtualenv path to'g'ri ko'rsatilgan
- [ ] Static files paths qo'shilgan
- [ ] Web app reload qilingan
- [ ] Sayt ishlayapti

---

**Muvaffaqiyat! 🚀**

