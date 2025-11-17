# Django Admin - Superuser Yaratish

## ✅ Sayt Ishlayapti!

Django admin sahifasi ochildi - bu yaxshi belgi! Endi superuser yaratishingiz kerak.

## 🔐 Superuser Yaratish

### Bash Console orqali:

1. Dashboard > "Files" tab ga kiring
2. "Bash console" ni oching
3. Quyidagi buyruqlarni bajaring:

```bash
cd ~/Uztoziya
source venv/bin/activate
python manage.py createsuperuser
```

4. Quyidagi ma'lumotlarni kiriting:
   - **Username**: o'zingiz xohlagan username (masalan: `admin`)
   - **Email address**: email manzilingiz (ixtiyoriy)
   - **Password**: kuchli parol kiriting (2 marta)

5. Superuser yaratilgandan keyin, admin sahifasiga qaytib, login qiling.

## 🔑 Mavjud Superuser Parolini O'zgartirish

Agar superuser allaqachon mavjud bo'lsa, lekin parolni unutgan bo'lsangiz:

```bash
cd ~/Uztoziya
source venv/bin/activate
python manage.py changepassword admin
```

Bu yerda `admin` o'rniga o'z username ingizni qo'ying.

## 📝 Boshqa Foydalanuvchilar Yaratish

Agar boshqa foydalanuvchilar yaratmoqchi bo'lsangiz:

1. Admin panelga kiring
2. "Users" bo'limiga kiring
3. "Add user" tugmasini bosing
4. Ma'lumotlarni to'ldiring

## 🎯 Keyingi Qadamlar

1. ✅ Superuser yaratildi
2. ✅ Admin panelga kirildi
3. ⬜ Database ma'lumotlarini to'ldirish
4. ⬜ Materiallar, testlar va boshqa ma'lumotlarni qo'shish

---

**Muvaffaqiyat! 🚀**

