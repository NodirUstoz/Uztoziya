from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OCRProcessing(models.Model):
    """OCR qayta ishlash jarayonlari"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Qayta ishlanmoqda'),
        ('completed', 'Tugatilgan'),
        ('failed', 'Xatolik'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ocr_processings',
        verbose_name='Foydalanuvchi'
    )
    test = models.ForeignKey(
        'tests.Test',
        on_delete=models.CASCADE,
        related_name='ocr_processings',
        verbose_name='Test',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='ocr_images/',
        verbose_name='Rasm'
    )
    processed_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Qayta ishlangan matn'
    )
    confidence_score = models.FloatField(
        default=0.0,
        verbose_name='Ishonch darajasi'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Holat'
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='Xatolik xabari'
    )
    processing_time = models.FloatField(
        default=0.0,
        verbose_name='Qayta ishlash vaqti (soniya)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tugatilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'OCR qayta ishlash'
        verbose_name_plural = 'OCR qayta ishlashlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OCR - {self.user.get_full_name()} ({self.status})"


class TestResult(models.Model):
    """Test natijalari (OCR orqali)"""
    
    ocr_processing = models.OneToOneField(
        OCRProcessing,
        on_delete=models.CASCADE,
        related_name='test_result',
        verbose_name='OCR qayta ishlash'
    )
    student_name = models.CharField(
        max_length=100,
        verbose_name='O\'quvchi ismi'
    )
    student_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Sinf'
    )
    total_questions = models.PositiveIntegerField(
        default=0,
        verbose_name='Jami savollar'
    )
    correct_answers = models.PositiveIntegerField(
        default=0,
        verbose_name='To\'g\'ri javoblar'
    )
    wrong_answers = models.PositiveIntegerField(
        default=0,
        verbose_name='Noto\'g\'ri javoblar'
    )
    score = models.PositiveIntegerField(
        default=0,
        verbose_name='Ball'
    )
    percentage = models.FloatField(
        default=0.0,
        verbose_name='Foiz'
    )
    grade = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Baholash'
    )
    processed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Qayta ishlangan vaqt'
    )
    
    class Meta:
        verbose_name = 'Test natijasi'
        verbose_name_plural = 'Test natijalari'
        ordering = ['-processed_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.score} ball ({self.percentage}%)"


class ExcelExport(models.Model):
    """Excel eksport fayllari"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='excel_exports',
        verbose_name='Foydalanuvchi'
    )
    test = models.ForeignKey(
        'tests.Test',
        on_delete=models.CASCADE,
        related_name='excel_exports',
        verbose_name='Test'
    )
    file = models.FileField(
        upload_to='excel_exports/',
        verbose_name='Excel fayl'
    )
    total_students = models.PositiveIntegerField(
        default=0,
        verbose_name='Jami o\'quvchilar soni'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'Excel eksport'
        verbose_name_plural = 'Excel eksportlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Excel - {self.test.title} ({self.total_students} o'quvchi)"