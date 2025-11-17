from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Kengaytirilgan foydalanuvchi modeli"""
    
    ROLE_CHOICES = [
        ('teacher', 'O\'qituvchi'),
        ('admin', 'Administrator'),
    ]
    
    SUBJECT_CHOICES = [
        ('mathematics', 'Matematika'),
        ('physics', 'Fizika'),
        ('chemistry', 'Kimyo'),
        ('biology', 'Biologiya'),
        ('geography', 'Geografiya'),
        ('history', 'Tarix'),
        ('literature', 'Adabiyot'),
        ('language', 'Til va adabiyot'),
        ('english', 'Ingliz tili'),
        ('russian', 'Rus tili'),
        ('computer_science', 'Informatika'),
        ('art', 'San\'at'),
        ('physical_education', 'Jismoniy tarbiya'),
        ('other', 'Boshqa'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='teacher',
        verbose_name='Rol'
    )
    
    subject = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES,
        verbose_name='Fan'
    )
    
    school = models.CharField(
        max_length=200,
        verbose_name='Maktab'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefon raqami'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biografiya'
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Tasdiqlangan'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan vaqt'
    )
    
    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_subject_display()})"
    
    def get_full_name(self):
        """To'liq ismni qaytaradi"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username