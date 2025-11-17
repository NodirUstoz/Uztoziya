from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TestCategory(models.Model):
    """Test kategoriyalari"""
    
    name = models.CharField(max_length=100, verbose_name='Kategoriya nomi')
    description = models.TextField(blank=True, null=True, verbose_name='Tavsif')
    
    class Meta:
        verbose_name = 'Test kategoriyasi'
        verbose_name_plural = 'Test kategoriyalari'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Test(models.Model):
    """Testlar"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', 'O\'rta'),
        ('hard', 'Qiyin'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Test sarlavhasi')
    description = models.TextField(verbose_name='Test tavsifi')
    category = models.ForeignKey(
        TestCategory,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Kategoriya'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Muallif'
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='Qiyinlik darajasi'
    )
    grade_level = models.CharField(
        max_length=50,
        verbose_name='Sinf darajasi'
    )
    subject = models.CharField(
        max_length=50,
        verbose_name='Fan'
    )
    time_limit = models.PositiveIntegerField(
        default=60,
        verbose_name='Vaqt chegarasi (daqiqa)'
    )
    total_questions = models.PositiveIntegerField(
        default=0,
        verbose_name='Jami savollar soni'
    )
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name='Jami ball'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Umumiy foydalanish'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol'
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
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """Test savollari"""
    
    QUESTION_TYPE_CHOICES = [
        ('single_choice', 'Bitta javob tanlash'),
        ('multiple_choice', 'Bir nechta javob tanlash'),
        ('true_false', 'To\'g\'ri/Noto\'g\'ri'),
        ('fill_blank', 'Bo\'sh joyni to\'ldirish'),
        ('essay', 'Erkin javob'),
    ]
    
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Test'
    )
    question_text = models.TextField(verbose_name='Savol matni')
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='single_choice',
        verbose_name='Savol turi'
    )
    points = models.PositiveIntegerField(
        default=1,
        verbose_name='Ball'
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name='Tartib raqami'
    )
    explanation = models.TextField(
        blank=True,
        null=True,
        verbose_name='Tushuntirish'
    )
    image = models.ImageField(
        upload_to='question_images/',
        blank=True,
        null=True,
        verbose_name='Savol rasmi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.test.title} - {self.question_text[:50]}..."


class Answer(models.Model):
    """Javob variantlari"""
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Savol'
    )
    answer_text = models.TextField(verbose_name='Javob matni')
    is_correct = models.BooleanField(
        default=False,
        verbose_name='To\'g\'ri javob'
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name='Tartib raqami'
    )
    
    class Meta:
        verbose_name = 'Javob'
        verbose_name_plural = 'Javoblar'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.answer_text[:30]}..."


class TestAttempt(models.Model):
    """Test topshirishlar"""
    
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Test'
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
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Boshlangan vaqt'
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tugatilgan vaqt'
    )
    score = models.PositiveIntegerField(
        default=0,
        verbose_name='Olingan ball'
    )
    percentage = models.FloatField(
        default=0.0,
        verbose_name='Foiz'
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name='Tugatilgan'
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='IP manzil'
    )
    
    class Meta:
        verbose_name = 'Test topshirish'
        verbose_name_plural = 'Test topshirishlar'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.test.title} - {self.student_name}"


class StudentAnswer(models.Model):
    """O'quvchi javoblari"""
    
    attempt = models.ForeignKey(
        TestAttempt,
        on_delete=models.CASCADE,
        related_name='student_answers',
        verbose_name='Test topshirish'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='student_answers',
        verbose_name='Savol'
    )
    selected_answers = models.ManyToManyField(
        Answer,
        related_name='student_selections',
        verbose_name='Tanlangan javoblar'
    )
    text_answer = models.TextField(
        blank=True,
        null=True,
        verbose_name='Matnli javob'
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='To\'g\'ri'
    )
    points_earned = models.PositiveIntegerField(
        default=0,
        verbose_name='Olingan ball'
    )
    answered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Javob berilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'O\'quvchi javobi'
        verbose_name_plural = 'O\'quvchi javoblari'
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.student_name} - {self.question.question_text[:30]}..."