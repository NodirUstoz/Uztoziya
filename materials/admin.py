from django.contrib import admin
from .models import (
    Material, MaterialCategory, MaterialRating, MaterialDownload,
    Assignment, StudentSubmission, VideoLesson, Model3D
)


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']
    list_filter = ['name']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'category', 'author', 'grade_level', 'is_public', 'download_count', 'rating', 'created_at']
    list_filter = ['material_type', 'category', 'is_public', 'grade_level', 'created_at']
    search_fields = ['title', 'description', 'tags']
    readonly_fields = ['download_count', 'rating', 'created_at', 'updated_at']


@admin.register(MaterialRating)
class MaterialRatingAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['material__title', 'user__first_name', 'user__last_name']


@admin.register(MaterialDownload)
class MaterialDownloadAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'downloaded_at', 'ip_address']
    list_filter = ['downloaded_at']
    search_fields = ['material__title', 'user__first_name', 'user__last_name']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'assignment_type', 'teacher', 'grade_level', 'subject', 'due_date', 'max_points', 'is_active', 'created_at']
    list_filter = ['assignment_type', 'grade_level', 'subject', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'instructions']
    filter_horizontal = ['materials']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student_name', 'student_class', 'status', 'grade', 'submitted_at', 'graded_at']
    list_filter = ['status', 'grade', 'submitted_at', 'graded_at']
    search_fields = ['student_name', 'student_email', 'assignment__title']
    filter_horizontal = ['attached_files']
    readonly_fields = ['created_at', 'submitted_at', 'graded_at']


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'grade_level', 'subject', 'duration', 'view_count', 'rating', 'is_public', 'created_at']
    list_filter = ['grade_level', 'subject', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'tags']
    readonly_fields = ['view_count', 'rating', 'created_at']


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ['title', 'model_type', 'author', 'category', 'grade_level', 'subject', 'file_size', 'is_interactive', 'is_public', 'download_count', 'rating', 'created_at']
    list_filter = ['model_type', 'grade_level', 'subject', 'is_interactive', 'is_public', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['download_count', 'rating', 'created_at']
