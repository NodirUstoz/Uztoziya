from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class MaterialCategory(models.Model):
    """Material kategoriyalari"""
    
    name = models.CharField(max_length=100, verbose_name='Kategoriya nomi')
    description = models.TextField(blank=True, null=True, verbose_name='Tavsif')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ikona')
    
    class Meta:
        verbose_name = 'Material kategoriyasi'
        verbose_name_plural = 'Material kategoriyalari'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Material(models.Model):
    """Ta'lim materiallari"""
    
    MATERIAL_TYPE_CHOICES = [
        ('presentation', 'PPT taqdimot'),
        ('document', 'Word hujjat'),
        ('handout', 'Tarqatma material'),
        ('worksheet', 'Ish varaqasi'),
        ('test', 'Test'),
        ('methodology', 'Metodika'),
        ('fact', 'Qiziqarli fakt'),
        ('video', 'Video darslik'),
        ('audio', 'Audio material'),
        ('image', 'Rasm galereyasi'),
        ('3d_model', '3D model'),
        ('interactive', 'Interaktiv material'),
        ('simulation', 'Simulyatsiya'),
        ('animation', 'Animatsiya'),
        ('other', 'Boshqa'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    description = models.TextField(verbose_name='Tavsif')
    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPE_CHOICES,
        verbose_name='Material turi'
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='Kategoriya'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='Muallif'
    )
    file = models.FileField(
        upload_to='materials/',
        verbose_name='Fayl'
    )
    thumbnail = models.ImageField(
        upload_to='material_thumbnails/',
        blank=True,
        null=True,
        verbose_name='Kichik rasm'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Teglar (vergul bilan ajrating)'
    )
    grade_level = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Sinf darajasi'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Umumiy foydalanish'
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Yuklab olishlar soni'
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name='Reyting'
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
        verbose_name = 'Material'
        verbose_name_plural = 'Materiallar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Teglarni ro'yxat ko'rinishida qaytaradi"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class MaterialRating(models.Model):
    """Material reytinglari"""
    
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Material'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='material_ratings',
        verbose_name='Foydalanuvchi'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Reyting'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Izoh'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'Material reytingi'
        verbose_name_plural = 'Material reytinglari'
        unique_together = ['material', 'user']
    
    def __str__(self):
        return f"{self.material.title} - {self.user.get_full_name()} ({self.rating})"


class MaterialDownload(models.Model):
    """Material yuklab olishlar tarixi"""
    
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='downloads',
        verbose_name='Material'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='material_downloads',
        verbose_name='Foydalanuvchi'
    )
    downloaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yuklab olingan vaqt'
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='IP manzil'
    )
    
    class Meta:
        verbose_name = 'Material yuklab olish'
        verbose_name_plural = 'Material yuklab olishlar'
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.material.title} - {self.user.get_full_name()}"


class Assignment(models.Model):
    """O'qituvchi tomonidan berilgan topshiriqlar"""
    
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Uy vazifasi'),
        ('classwork', 'Dars ishi'),
        ('project', 'Loyiha'),
        ('research', 'Tadqiqot'),
        ('presentation', 'Taqdimot'),
        ('test_assignment', 'Test topshirish'),
        ('creative', 'Ijodiy ish'),
        ('practical', 'Amaliy ish'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Topshiriq sarlavhasi')
    description = models.TextField(verbose_name='Topshiriq tavsifi')
    assignment_type = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_TYPE_CHOICES,
        verbose_name='Topshiriq turi'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        verbose_name='O\'qituvchi'
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Kategoriya'
    )
    grade_level = models.CharField(
        max_length=50,
        verbose_name='Sinf darajasi'
    )
    subject = models.CharField(
        max_length=50,
        verbose_name='Fan'
    )
    due_date = models.DateTimeField(
        verbose_name='Topshiriq muddati'
    )
    max_points = models.PositiveIntegerField(
        default=100,
        verbose_name='Maksimal ball'
    )
    materials = models.ManyToManyField(
        Material,
        blank=True,
        related_name='assignments',
        verbose_name='Kerakli materiallar'
    )
    instructions = models.TextField(
        blank=True,
        null=True,
        verbose_name='Qo\'shimcha ko\'rsatmalar'
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
        verbose_name = 'Topshiriq'
        verbose_name_plural = 'Topshiriqlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class StudentSubmission(models.Model):
    """O'quvchi tomonidan topshirilgan ishlar"""
    
    SUBMISSION_STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('submitted', 'Topshirilgan'),
        ('graded', 'Baholangan'),
        ('returned', 'Qaytarilgan'),
    ]
    
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Topshiriq'
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
    student_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='O\'quvchi email'
    )
    submission_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Matnli javob'
    )
    attached_files = models.ManyToManyField(
        Material,
        blank=True,
        related_name='submission_attachments',
        verbose_name='Ilova fayllar'
    )
    status = models.CharField(
        max_length=20,
        choices=SUBMISSION_STATUS_CHOICES,
        default='draft',
        verbose_name='Holat'
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Topshirilgan vaqt'
    )
    grade = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Olingan ball'
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name='O\'qituvchi izohi'
    )
    graded_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Baholangan vaqt'
    )
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='graded_submissions',
        verbose_name='Baholagan o\'qituvchi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'O\'quvchi topshirig\'i'
        verbose_name_plural = 'O\'quvchi topshirig\'lari'
        ordering = ['-submitted_at']
        unique_together = ['assignment', 'student_email']
    
    def __str__(self):
        return f"{self.assignment.title} - {self.student_name}"


class VideoLesson(models.Model):
    """Video darsliklar"""
    
    title = models.CharField(max_length=200, verbose_name='Darslik sarlavhasi')
    description = models.TextField(verbose_name='Darslik tavsifi')
    video_file = models.FileField(
        upload_to='video_lessons/',
        verbose_name='Video fayl'
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        blank=True,
        null=True,
        verbose_name='Video rasmi'
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name='Davomiyligi (soniya)'
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        related_name='video_lessons',
        verbose_name='Kategoriya'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='video_lessons',
        verbose_name='Muallif'
    )
    grade_level = models.CharField(
        max_length=50,
        verbose_name='Sinf darajasi'
    )
    subject = models.CharField(
        max_length=50,
        verbose_name='Fan'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Teglar'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Umumiy foydalanish'
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Ko\'rilganlar soni'
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name='Reyting'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = 'Video darslik'
        verbose_name_plural = 'Video darsliklar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Model3D(models.Model):
    """3D modellar"""
    
    MODEL_TYPE_CHOICES = [
        ('educational', 'Ta\'limiy'),
        ('scientific', 'Ilmiy'),
        ('historical', 'Tarixiy'),
        ('biological', 'Biologik'),
        ('geological', 'Geologik'),
        ('architectural', 'Arxitektura'),
        ('artistic', 'Badiiy'),
        ('technical', 'Texnik'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Model sarlavhasi')
    description = models.TextField(verbose_name='Model tavsifi')
    model_file = models.FileField(
        upload_to='3d_models/',
        verbose_name='3D model fayli'
    )
    thumbnail = models.ImageField(
        upload_to='3d_thumbnails/',
        blank=True,
        null=True,
        verbose_name='Model rasmi'
    )
    model_type = models.CharField(
        max_length=20,
        choices=MODEL_TYPE_CHOICES,
        verbose_name='Model turi'
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        related_name='models_3d',
        verbose_name='Kategoriya'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='models_3d',
        verbose_name='Muallif'
    )
    grade_level = models.CharField(
        max_length=50,
        verbose_name='Sinf darajasi'
    )
    subject = models.CharField(
        max_length=50,
        verbose_name='Fan'
    )
    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name='Fayl hajmi (bayt)'
    )
    is_interactive = models.BooleanField(
        default=False,
        verbose_name='Interaktiv'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Umumiy foydalanish'
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Yuklab olishlar soni'
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name='Reyting'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    class Meta:
        verbose_name = '3D model'
        verbose_name_plural = '3D modellar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title