from rest_framework import serializers
from .models import (
    Material, MaterialCategory, MaterialRating, MaterialDownload,
    Assignment, StudentSubmission, VideoLesson, Model3D
)


class MaterialCategorySerializer(serializers.ModelSerializer):
    """Material kategoriya serializeri"""
    
    materials_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialCategory
        fields = ['id', 'name', 'description', 'icon', 'materials_count']
    
    def get_materials_count(self, obj):
        """Kategoriyadagi materiallar soni"""
        return obj.materials.filter(is_public=True).count()


class MaterialSerializer(serializers.ModelSerializer):
    """Material serializeri"""
    
    author_name = serializers.SerializerMethodField()
    author_subject = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    material_type_display = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = [
            'id', 'title', 'description', 'material_type', 'material_type_display',
            'category', 'category_name', 'author', 'author_name', 'author_subject',
            'file', 'file_url', 'thumbnail', 'thumbnail_url', 'tags', 'tags_list',
            'grade_level', 'is_public', 'download_count', 'rating', 'ratings_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'download_count', 'rating', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        """Muallif nomini qaytaradi"""
        return obj.author.get_full_name()
    
    def get_author_subject(self, obj):
        """Muallif fanini qaytaradi"""
        return obj.author.get_subject_display()
    
    def get_category_name(self, obj):
        """Kategoriya nomini qaytaradi"""
        return obj.category.name if obj.category else None
    
    def get_file_url(self, obj):
        """Fayl URL ini qaytaradi"""
        if obj.file:
            return obj.file.url
        return None
    
    def get_thumbnail_url(self, obj):
        """Kichik rasm URL ini qaytaradi"""
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
    
    def get_tags_list(self, obj):
        """Teglarni ro'yxat ko'rinishida qaytaradi"""
        return obj.get_tags_list()
    
    def get_material_type_display(self, obj):
        """Material turi nomini qaytaradi"""
        return obj.get_material_type_display()
    
    def get_ratings_count(self, obj):
        """Reytinglar soni"""
        return obj.ratings.count()


class MaterialRatingSerializer(serializers.ModelSerializer):
    """Material reyting serializeri"""
    
    user_name = serializers.SerializerMethodField()
    material_title = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialRating
        fields = [
            'id', 'material', 'material_title', 'user', 'user_name',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_user_name(self, obj):
        """Foydalanuvchi nomini qaytaradi"""
        return obj.user.get_full_name()
    
    def get_material_title(self, obj):
        """Material sarlavhasini qaytaradi"""
        return obj.material.title


class MaterialDownloadSerializer(serializers.ModelSerializer):
    """Material yuklab olish serializeri"""
    
    user_name = serializers.SerializerMethodField()
    material_title = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialDownload
        fields = [
            'id', 'material', 'material_title', 'user', 'user_name',
            'downloaded_at', 'ip_address'
        ]
        read_only_fields = ['id', 'downloaded_at']
    
    def get_user_name(self, obj):
        """Foydalanuvchi nomini qaytaradi"""
        return obj.user.get_full_name()
    
    def get_material_title(self, obj):
        """Material sarlavhasini qaytaradi"""
        return obj.material.title


class MaterialCreateSerializer(serializers.ModelSerializer):
    """Material yaratish serializeri"""
    
    class Meta:
        model = Material
        fields = [
            'title', 'description', 'material_type', 'category',
            'file', 'thumbnail', 'tags', 'grade_level', 'is_public'
        ]
    
    def validate_file(self, value):
        """Fayl hajmini tekshirish"""
        if value.size > 50 * 1024 * 1024:  # 50MB
            raise serializers.ValidationError("Fayl hajmi 50MB dan katta bo'lmasligi kerak")
        return value
    
    def validate_tags(self, value):
        """Teglarni tozalash"""
        if value:
            # Vergul bilan ajratilgan tegni tozalash
            tags = [tag.strip() for tag in value.split(',') if tag.strip()]
            return ', '.join(tags)
        return value


class AssignmentSerializer(serializers.ModelSerializer):
    """Topshiriq serializeri"""
    
    teacher_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    assignment_type_display = serializers.SerializerMethodField()
    submissions_count = serializers.SerializerMethodField()
    materials_list = MaterialSerializer(source='materials', many=True, read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'assignment_type', 'assignment_type_display',
            'teacher', 'teacher_name', 'category', 'category_name', 'grade_level',
            'subject', 'due_date', 'max_points', 'materials', 'materials_list',
            'instructions', 'is_active', 'submissions_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'teacher', 'created_at', 'updated_at']
    
    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_assignment_type_display(self, obj):
        return obj.get_assignment_type_display()
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()


class StudentSubmissionSerializer(serializers.ModelSerializer):
    """O'quvchi topshirig'i serializeri"""
    
    assignment_title = serializers.SerializerMethodField()
    graded_by_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    attached_files_list = MaterialSerializer(source='attached_files', many=True, read_only=True)
    
    class Meta:
        model = StudentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'student_name', 'student_class',
            'student_email', 'submission_text', 'attached_files', 'attached_files_list',
            'status', 'status_display', 'submitted_at', 'grade', 'feedback',
            'graded_at', 'graded_by', 'graded_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'graded_at', 'graded_by', 'created_at']
    
    def get_assignment_title(self, obj):
        return obj.assignment.title
    
    def get_graded_by_name(self, obj):
        return obj.graded_by.get_full_name() if obj.graded_by else None
    
    def get_status_display(self, obj):
        return obj.get_status_display()


class VideoLessonSerializer(serializers.ModelSerializer):
    """Video darslik serializeri"""
    
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoLesson
        fields = [
            'id', 'title', 'description', 'video_file', 'video_url', 'thumbnail',
            'thumbnail_url', 'duration', 'duration_formatted', 'category',
            'category_name', 'author', 'author_name', 'grade_level', 'subject',
            'tags', 'tags_list', 'is_public', 'view_count', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'view_count', 'rating', 'created_at']
    
    def get_author_name(self, obj):
        return obj.author.get_full_name()
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_video_url(self, obj):
        if obj.video_file:
            return obj.video_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
    
    def get_tags_list(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []
    
    def get_duration_formatted(self, obj):
        minutes = obj.duration // 60
        seconds = obj.duration % 60
        return f"{minutes:02d}:{seconds:02d}"


class Model3DSerializer(serializers.ModelSerializer):
    """3D model serializeri"""
    
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    model_type_display = serializers.SerializerMethodField()
    model_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Model3D
        fields = [
            'id', 'title', 'description', 'model_file', 'model_url', 'thumbnail',
            'thumbnail_url', 'model_type', 'model_type_display', 'category',
            'category_name', 'author', 'author_name', 'grade_level', 'subject',
            'file_size', 'file_size_formatted', 'is_interactive', 'is_public',
            'download_count', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'download_count', 'rating', 'created_at']
    
    def get_author_name(self, obj):
        return obj.author.get_full_name()
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_model_type_display(self, obj):
        return obj.get_model_type_display()
    
    def get_model_url(self, obj):
        if obj.model_file:
            return obj.model_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None
    
    def get_file_size_formatted(self, obj):
        """Fayl hajmini formatlash"""
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
