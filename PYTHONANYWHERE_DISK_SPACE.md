# Disk Joyini Bo'shatish - PythonAnywhere

## Muammo

Disk kvotasi tugab qolgan (512 MB limit, 75% to'ldirilgan).

## Yechimlar

### 1. Diskda Nima Ko'p Joy Egallayotganini Tekshirish

```bash
cd ~
du -sh * | sort -h
```

Bu buyruq har bir papkaning hajmini ko'rsatadi.

### 2. Virtualenv ni Tozalash

```bash
cd ~/Uztoziya
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Keraksiz Paketlarni Olib Tashlash

`requirements.txt` dan quyidagilarni vaqtincha olib tashlash mumkin (agar hozircha kerak bo'lmasa):

- `mysqlclient==2.2.0` - SQLite ishlatmoqchi bo'lsangiz
- `celery==5.3.4` - agar background tasks kerak bo'lmasa
- `redis==5.0.1` - agar celery ishlatmasangiz
- `google-cloud-vision==3.11.0` - agar OCR kerak bo'lmasa
- `opencv-python==4.8.1.78` - agar image processing kerak bo'lmasa

### 4. Minimal Requirements.txt Yaratish

Asosiy paketlar uchun minimal `requirements.txt`:

```txt
Django==4.2.7
Pillow==11.0.0
django-cors-headers==4.3.1
djangorestframework==3.14.0
python-decouple==3.8
whitenoise==6.6.0
dj-database-url==2.1.0
```

### 5. .git Papkasini Tekshirish

```bash
cd ~/Uztoziya
du -sh .git
```

Agar .git katta bo'lsa, uni o'chirib tashlash mumkin (agar GitHub ga push qilgan bo'lsangiz).

### 6. Cache va Temporary Fayllarni Tozalash

```bash
cd ~/Uztoziya
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
rm -rf venv/lib/python*/site-packages/*/tests
```

### 7. Minimal Paketlar O'rnatish

Avval asosiy paketlarni o'rnating:

```bash
cd ~/Uztoziya
source venv/bin/activate
pip install Django==4.2.7
pip install Pillow==11.0.0
pip install django-cors-headers==4.3.1
pip install djangorestframework==3.14.0
pip install python-decouple==3.8
pip install whitenoise==6.6.0
pip install dj-database-url==2.1.0
```

Keyin qolgan paketlarni kerak bo'lganda qo'shing.

---

**Tavsiya**: Avval disk joyini bo'shating, keyin minimal paketlarni o'rnating.

