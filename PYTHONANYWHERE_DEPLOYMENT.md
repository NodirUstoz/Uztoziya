# PythonAnywhere ga Deploy Qilish Qo'llanmasi

Bu qo'llanma Ustoziya platformasini PythonAnywhere ga deploy qilish uchun yozilgan.

## 📋 Talablar

1. PythonAnywhere account (https://www.pythonanywhere.com)
   - Free account yoki paid account
   - Free account da cheklovlar bor (1 web app, cheklangan CPU vaqti)
2. GitHub repository (loyiha GitHub da bo'lishi kerak) yoki manual upload
3. Barcha API kalitlar (OpenAI, Google Gemini, va boshqalar)

## 🚀 Deploy Qadamlar

### 1. PythonAnywhere Account Yaratish

1. https://www.pythonanywhere.com ga kiring
2. "Beginner" yoki "Hacker" plan ni tanlang
3. Account yarating va login qiling

### 2. Files Tab - Loyihani Yuklash

#### Variant 1: GitHub orqali (Tavsiya etiladi)

1. Dashboard > "Files" tab ga kiring
2. "Bash console" ni oching
3. Quyidagi buyruqlarni bajaring:

```bash
cd ~
git clone https://github.com/yourusername/Uztoziya.git
# yoki o'z repository URL ingizni qo'ying
cd Uztoziya
```

#### Variant 2: Manual Upload

1. Dashboard > "Files" tab ga kiring
2. "Upload a file" tugmasini bosing
3. Barcha loyiha fayllarini yuklang
4. Yoki ZIP fayl yuklab, keyin extract qiling:

```bash
cd ~
unzip Uztoziya.zip
cd Uztoziya
```

### 3. Virtual Environment Yaratish

Bash console da:

```bash
cd ~/Uztoziya
python3.10 -m venv venv  # yoki python3.11
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Eslatma**: PythonAnywhere da Python versiyasini tekshiring:
```bash
python3.10 --version  # yoki python3.11
```

### 4. Database Sozlash

#### SQLite (Free account uchun - oson)

SQLite avtomatik ishlaydi, hech qanday sozlash kerak emas.

#### MySQL (PythonAnywhere da mavjud)

Agar MySQL ishlatmoqchi bo'lsangiz:

1. Dashboard > "Databases" tab ga kiring
2. MySQL database yarating
3. Database nomi, username va password ni saqlang
4. `settings.py` da database sozlamalarini yangilang:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$database_name',
        'USER': 'yourusername',
        'PASSWORD': 'your_password',
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**Eslatma**: `requirements.txt` ga `mysqlclient` qo'shing:
```
mysqlclient==2.2.0
```

### 5. Environment Variables Sozlash

#### Variant 1: .env fayl (Tavsiya etiladi)

1. Dashboard > "Files" tab > `Uztoziya` papkasiga kiring
2. `.env` fayl yarating
3. Quyidagi o'zgaruvchilarni qo'ying:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=
CORS_ALLOW_ALL_ORIGINS=False
TESSERACT_PATH=/usr/bin/tesseract

# API Keys
OPENAI_API_KEY=your-openai-key
GOOGLE_GEMINI_API_KEY=your-gemini-key
GOOGLE_API_KEY=your-google-api-key
OPENROUTER_API_KEY=your-openrouter-key
```

**Eslatma**: Secret key yaratish:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Variant 2: PythonAnywhere Environment Variables

1. Dashboard > "Web" tab ga kiring
2. "Environment variables" bo'limiga kiring
3. Har bir o'zgaruvchini qo'shing

### 6. Database Migration

Bash console da:

```bash
cd ~/Uztoziya
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Web App Sozlash

1. Dashboard > "Web" tab ga kiring
2. "Add a new web app" tugmasini bosing
3. Domain ni tanlang (masalan: `yourusername.pythonanywhere.com`)
4. "Manual configuration" ni tanlang
5. Python versiyasini tanlang (3.10 yoki 3.11)

### 8. WSGI Configuration

1. "Web" tab > "WSGI configuration file" linkini bosing
2. Barcha mavjud kodni o'chiring
3. Quyidagi kodni qo'ying (yoki `wsgi.py` faylini ochib, ichidagini ko'chiring):

```python
import os
import sys

# O'z username ingizni qo'ying
path = '/home/yourusername/Uztoziya'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ustoziya_platform.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Muhim**: `yourusername` ni o'z username ingizga almashtiring!

### 9. Static Files Sozlash

1. "Web" tab > "Static files" bo'limiga kiring
2. Quyidagi URL va Directory ni qo'shing:

- **URL**: `/static/`
- **Directory**: `/home/yourusername/Uztoziya/staticfiles`

- **URL**: `/media/`
- **Directory**: `/home/yourusername/Uztoziya/media`

### 10. Reload Web App

1. "Web" tab > "Reload" tugmasini bosing
2. Bir necha soniya kutib turing
3. Sizning domain ingizga kiring (masalan: `https://yourusername.pythonanywhere.com`)

## 🔧 Qo'shimcha Sozlamalar

### Scheduled Tasks (Cron Jobs)

Agar Celery yoki scheduled tasks ishlatmoqchi bo'lsangiz:

1. Dashboard > "Tasks" tab ga kiring
2. "Create a new task" ni bosing
3. Command ni kiriting:

```bash
cd /home/yourusername/Uztoziya && /home/yourusername/Uztoziya/venv/bin/python manage.py your_command
```

### Tesseract OCR

PythonAnywhere da Tesseract mavjud. Agar ishlamasa:

1. Bash console da:
```bash
pip install pytesseract
```

2. `settings.py` da:
```python
TESSERACT_PATH = '/usr/bin/tesseract'
```

### Media Files

Media files `media/` papkasida saqlanadi. Katta fayllar uchun:
- AWS S3 yoki boshqa cloud storage ishlatish tavsiya etiladi
- Yoki PythonAnywhere paid plan ga upgrade qiling

## 🐛 Muammolarni Hal Qilish

### 500 Internal Server Error

1. "Web" tab > "Error log" ni tekshiring
2. Xatolarni ko'ring va tuzating
3. "Reload" qiling

### Static Files Ko'rinmayapti

1. `collectstatic` bajarilganligini tekshiring
2. Static files path to'g'ri sozlanganligini tekshiring
3. "Reload" qiling

### Database Connection Xatosi

1. Database credentials to'g'ri ekanligini tekshiring
2. MySQL uchun: `mysqlclient` o'rnatilganligini tekshiring
3. SQLite uchun: fayl yozish huquqlari borligini tekshiring

### Import Error

1. Virtual environment aktiv ekanligini tekshiring
2. Barcha paketlar o'rnatilganligini tekshiring:
```bash
pip install -r requirements.txt
```

### Module Not Found

1. `sys.path` to'g'ri sozlanganligini tekshiring
2. Project path to'g'ri ekanligini tekshiring

## 📝 Eslatmalar

1. **Free Plan Cheklovlari**:
   - 1 web app
   - Cheklangan CPU vaqti
   - 3 ta external site ga so'rov
   - 512 MB disk space

2. **Production uchun Tavsiyalar**:
   - Paid plan ga upgrade qiling
   - Media files uchun cloud storage ishlating
   - Monitoring va logging qo'shing
   - Regular backups qiling

3. **Security**:
   - `DEBUG=False` production da
   - `SECRET_KEY` ni hech qachon commit qilmang
   - API keys ni environment variables orqali boshqaring
   - HTTPS ishlatish (PythonAnywhere avtomatik qo'llab-quvvatlaydi)

4. **Updates**:
   - Code yangilanganda "Reload" qiling
   - Database migration qiling: `python manage.py migrate`
   - Static files yangilanganda: `python manage.py collectstatic`

## 🔗 Foydali Linklar

- [PythonAnywhere Documentation](https://help.pythonanywhere.com/)
- [Django on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [PythonAnywhere Web App Setup](https://help.pythonanywhere.com/pages/WebApp/)

## ✅ Tekshirish Ro'yxati

Deploy qilishdan oldin:

- [ ] PythonAnywhere account yaratilgan
- [ ] Loyiha yuklangan
- [ ] Virtual environment yaratilgan va paketlar o'rnatilgan
- [ ] Database sozlangan
- [ ] Environment variables qo'shilgan
- [ ] Migrations bajarilgan
- [ ] Superuser yaratilgan
- [ ] Static files yig'ilgan
- [ ] WSGI configuration to'g'ri sozlangan
- [ ] Static files paths to'g'ri sozlangan
- [ ] Web app reload qilingan
- [ ] Test qilingan

---

**Muvaffaqiyatli deploy qilish tilaymiz! 🚀**

