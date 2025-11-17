# Render ga Deploy Qilish Qo'llanmasi

Bu qo'llanma Ustoziya platformasini Render ga deploy qilish uchun yozilgan.

## 📋 Talablar

1. Render account (https://render.com)
2. GitHub repository (loyiha GitHub da bo'lishi kerak)
3. Barcha API kalitlar (OpenAI, Google Gemini, va boshqalar)

## 🚀 Deploy Qadamlar

### 1. GitHub ga Push Qiling

Avval loyihani GitHub ga push qiling:

```bash
git add .
git commit -m "Render deployment uchun tayyorlandi"
git push origin main
```

### 2. Render Dashboard ga Kiring

1. https://render.com ga kiring
2. "New +" tugmasini bosing
3. "Blueprint" ni tanlang (yoki "Web Service" ni tanlang)

### 3. Database Yaratish

1. Render Dashboard da "New +" > "PostgreSQL" ni tanlang
2. Database nomi: `ustoziya-db`
3. Plan: Free
4. Database Name: `ustoziya`
5. User: `ustoziya`
6. "Create Database" ni bosing
7. Database yaratilgandan keyin, "Connections" bo'limidan `DATABASE_URL` ni ko'ring va saqlang

### 4. Web Service Yaratish

#### Variant 1: render.yaml orqali (Tavsiya etiladi)

1. Render Dashboard da "New +" > "Blueprint" ni tanlang
2. GitHub repository ni ulang
3. `render.yaml` faylini tanlang
4. Render avtomatik ravishda barcha servislarni yaratadi

#### Variant 2: Manual

1. Render Dashboard da "New +" > "Web Service" ni tanlang
2. GitHub repository ni ulang
3. Quyidagi sozlamalarni kiriting:
   - **Name**: `ustoziya`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn ustoziya_platform.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free

### 5. Environment Variables Qo'shish

Render Dashboard da Web Service > "Environment" bo'limiga quyidagi o'zgaruvchilarni qo'shing:

#### Majburiy:
- `DJANGO_SECRET_KEY` - Django secret key (yangi yarating: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` - `False`
- `DATABASE_URL` - PostgreSQL database URL (avtomatik yaratiladi agar database service bilan ulangan bo'lsa)
- `ALLOWED_HOSTS` - `ustoziya.onrender.com,*.onrender.com` (yoki o'z domain ingiz)

#### API Keys (ixtiyoriy, lekin tavsiya etiladi):
- `OPENAI_API_KEY` - OpenAI API kaliti
- `GOOGLE_GEMINI_API_KEY` - Google Gemini API kaliti
- `GOOGLE_API_KEY` - Google Cloud Vision API kaliti
- `OPENROUTER_API_KEY` - OpenRouter API kaliti

#### Boshqa (ixtiyoriy):
- `TESSERACT_PATH` - `/usr/bin/tesseract` (Linux uchun)
- `CORS_ALLOW_ALL_ORIGINS` - `True` yoki `False`

### 6. Database Migration

Agar database avtomatik migrate qilinmagan bo'lsa:

1. Render Dashboard da Web Service > "Shell" ni oching
2. Quyidagi buyruqlarni bajaring:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Static Files

Static files avtomatik ravishda `buildCommand` da `collectstatic` orqali yig'iladi.

## 🔧 Sozlash

### Custom Domain

Agar o'z domain ingizni ulamoqchi bo'lsangiz:

1. Render Dashboard > Web Service > "Settings" > "Custom Domains"
2. Domain ni qo'shing
3. DNS sozlamalarini yangilang
4. `ALLOWED_HOSTS` environment variable ni yangilang

### Media Files

Render free plan da media files saqlash uchun disk space cheklangan. Katta fayllar uchun:
- AWS S3 yoki boshqa cloud storage ishlatish tavsiya etiladi
- Yoki Render disk storage ni upgrade qilish

## 🐛 Muammolarni Hal Qilish

### Database Connection Xatosi

- `DATABASE_URL` to'g'ri sozlanganligini tekshiring
- Database service ishlamoqda ekanligini tekshiring

### Static Files Ko'rinmayapti

- `collectstatic` muvaffaqiyatli bajarilganligini tekshiring
- `STATIC_ROOT` to'g'ri sozlanganligini tekshiring
- WhiteNoise middleware qo'shilganligini tekshiring

### Migration Xatolari

- Database connection to'g'ri ekanligini tekshiring
- Migration fayllar to'g'ri ekanligini tekshiring
- Shell orqali manual migrate qiling

### Port Xatosi

- `$PORT` environment variable ishlatilganligini tekshiring
- Gunicorn to'g'ri sozlanganligini tekshiring

## 📝 Eslatmalar

1. **Free Plan Cheklovlari**:
   - 15 daqiqada ishlamay qolsa, uyquga ketadi
   - Birinchi so'rov sekin bo'lishi mumkin (cold start)
   - Disk space cheklangan

2. **Production uchun Tavsiyalar**:
   - Paid plan ga upgrade qiling
   - Media files uchun cloud storage ishlating
   - Redis va Celery uchun alohida servis yarating
   - Monitoring va logging qo'shing

3. **Security**:
   - `DEBUG=False` production da
   - `SECRET_KEY` ni hech qachon commit qilmang
   - API keys ni environment variables orqali boshqaring

## 🔗 Foydali Linklar

- [Render Documentation](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [PostgreSQL on Render](https://render.com/docs/databases)

## ✅ Tekshirish Ro'yxati

Deploy qilishdan oldin:

- [ ] `render.yaml` to'g'ri sozlangan
- [ ] `requirements.txt` yangilangan
- [ ] `settings.py` production uchun sozlangan
- [ ] Environment variables qo'shilgan
- [ ] Database yaratilgan
- [ ] Migrations bajarilgan
- [ ] Superuser yaratilgan
- [ ] Static files yig'ilgan
- [ ] Test qilingan

---

**Muvaffaqiyatli deploy qilish tilaymiz! 🚀**

