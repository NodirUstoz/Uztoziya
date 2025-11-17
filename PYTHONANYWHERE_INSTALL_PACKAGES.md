# Paketlarni O'rnatish - PythonAnywhere

## Muammo

Virtualenv aktiv, lekin Django va boshqa paketlar o'rnatilmagan.

## Yechim

Bash console da quyidagi buyruqlarni bajaring:

```bash
cd ~/Uztoziya
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Bu jarayon bir necha daqiqa davom etishi mumkin.

## Tekshirish

Paketlar o'rnatilgandan keyin:

```bash
python -c "import django; print(django.get_version())"
```

Agar Django versiyasini ko'rsatsa - hammasi yaxshi!

## Keyin Database Migration

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

**Eslatma**: Agar `mysqlclient` o'rnatishda muammo bo'lsa, uni o'chirib tashlashingiz mumkin (SQLite ishlatmoqchi bo'lsangiz).

