# Ustoziya Platformasi - Ta'lim Materiallari Platformasi

Bu Django asosidagi ta'lim materiallari platformasi bo'lib, o'qituvchilar uchun PPT taqdimotlar, testlar, tarqatma materiallar, video darsliklar va 3D modellarni boshqarish imkonini beradi.

## 🚀 Xususiyatlari

### 📚 Asosiy Bo'limlar

1. **Materiallar**
   - PPT taqdimotlar
   - Word hujjatlar
   - Tarqatma materiallar
   - Ish varaqalari
   - Metodikalar
   - Qiziqarli faktlar

2. **Topshiriqlar Tizimi**
   - O'qituvchi tomonidan topshiriq berish
   - O'quvchi tomonidan ishni topshirish
   - Avtomatik baholash
   - Izohlar va tushuntirishlar

3. **Video Darsliklar**
   - Video fayllarni yuklash
   - Video ko'rish statistikasi
   - Kategoriyalar bo'yicha tashkil etish
   - Teglar orqali qidirish

4. **3D Modellar**
   - 3D model fayllarni yuklash
   - Interaktiv modellar
   - Turli formatlar (OBJ, FBX, DAE, GLTF, GLB, PLY, STL)
   - Model reytinglari

5. **Testlar**
   - Turli savol turlari
   - Avtomatik baholash
   - Natijalarni eksport qilish
   - Statistika

6. **OCR Tekshirish**
   - Rasm orqali matnni o'qish
   - AI yordamida tahlil
   - Natijalarni saqlash

### 🎯 Foydalanuvchi Rollari

- **O'qituvchi**: Materiallar yaratish, topshiriqlar berish, baholash
- **O'quvchi**: Materiallarni yuklab olish, topshiriqlarni bajarish
- **Admin**: Tizimni boshqarish

## 🛠 Texnologiyalar

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: Google Gemini AI, Tesseract OCR, Google Cloud Vision
- **Media**: Video, Audio, 3D model fayllar

## 📦 O'rnatish

### Talablar
- Python 3.8+
- Django 5.2+
- Tesseract OCR
- Google Cloud Vision API kaliti

### Qadamlar

1. **Loyihani klonlash**
```bash
git clone <repository-url>
cd ustoziya_new
```

2. **Virtual environment yaratish**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

3. **Kerakli paketlarni o'rnatish**
```bash
pip install -r requirements.txt
```

4. **Ma'lumotlar bazasini sozlash**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Superuser yaratish**
```bash
python manage.py createsuperuser
```

6. **Serverni ishga tushirish**
```bash
python manage.py runserver
```

## 🔧 Sozlash

### Environment Variables
`.env` fayl yarating va quyidagi o'zgaruvchilarni qo'shing:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

# OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_CHAT_MODEL=gpt-4o-mini        # ixtiyoriy, default shu
OPENAI_IMAGE_MODEL=gpt-image-1       # ixtiyoriy

# Google Gemini
GOOGLE_GEMINI_API_KEY=your-gemini-api-key
GOOGLE_GEMINI_MODEL=models/gemini-1.5-flash-latest  # ixtiyoriy

# OpenRouter
OPENROUTER_API_KEY=your-openrouter-key          # talab qilinadi, agar OpenRouter ishlatilsa
OPENROUTER_MODEL=openai/gpt-4o                  # ixtiyoriy
OPENROUTER_SITE_URL=http://127.0.0.1:8000       # OpenRouter statistikasi uchun
OPENROUTER_SITE_NAME=Ustoziya Platformasi      # OpenRouter statistikasi uchun

# Boshqa servislar
GOOGLE_API_KEY=your-google-api-key
GOOGLE_PROJECT_ID=your-project-id
TESSERACT_PATH=/path/to/tesseract
```

### Media Files
`settings.py` faylida media fayllar uchun sozlamalarni tekshiring:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 📱 API Endpoints

### Materiallar
- `GET /api/materials/` - Materiallar ro'yxati
- `POST /api/materials/` - Yangi material yaratish
- `GET /api/materials/{id}/` - Material tafsilotlari
- `PUT /api/materials/{id}/` - Materialni yangilash
- `DELETE /api/materials/{id}/` - Materialni o'chirish

### Topshiriqlar
- `GET /api/materials/assignments/` - Topshiriqlar ro'yxati
- `POST /api/materials/assignments/` - Yangi topshiriq yaratish
- `GET /api/materials/assignments/{id}/` - Topshiriq tafsilotlari

### Video Darsliklar
- `GET /api/materials/videos/` - Video darsliklar ro'yxati
- `POST /api/materials/videos/` - Yangi video yaratish
- `GET /api/materials/videos/{id}/watch/` - Video ko'rish

### 3D Modellar
- `GET /api/materials/3d-models/` - 3D modellar ro'yxati
- `POST /api/materials/3d-models/` - Yangi model yaratish
- `GET /api/materials/3d-models/{id}/download/` - Modelni yuklab olish

## 🎨 Interface

Platforma zamonaviy va foydalanuvchi-do'st interfeysga ega:
- Responsive dizayn
- Bootstrap 5 komponentlari
- Font Awesome ikonkalar
- Gradient ranglar va animatsiyalar
- Mobile-friendly

## 📊 Statistika va Hisobot

- Foydalanuvchi faoliyati
- Materiallar statistikasi
- Test natijalari
- Yuklab olishlar soni
- Reytinglar va izohlar

## 🔐 Xavfsizlik

- Django authentication
- CSRF protection
- File upload validation
- User permissions
- Secure file handling

## 🚀 Production Deployment

### Docker (ixtiyoriy)
```bash
docker build -t ustoziya-platform .
docker run -p 8000:8000 ustoziya-platform
```

### Nginx + Gunicorn
```bash
pip install gunicorn
gunicorn ustoziya_platform.wsgi:application --bind 0.0.0.0:8000
```

## 🤝 Hissa Qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request yarating

## 📝 License

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## 📞 Aloqa

- Email: info@ustoziya.uz
- Website: https://ustoziya.uz
- Telegram: @ustoziya_support

## 🙏 Minnatdorchilik

- Django jamoasiga
- Bootstrap jamoasiga
- Font Awesome jamoasiga
- Barcha open source loyihalar uchun

---

**Ustoziya Platformasi** - Ta'limni yangi darajaga ko'tarish uchun!
