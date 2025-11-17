from django.contrib import admin
from .models import TestCategory, Test, Question, Answer, TestAttempt, StudentAnswer

# Register your models here.
@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'subject', 'difficulty', 'is_public', 'is_active', 'created_at']
    list_filter = ['category', 'subject', 'difficulty', 'is_public', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'test', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'test__category']
    search_fields = ['question_text']
    ordering = ['test', 'order']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__test__category']
    search_fields = ['answer_text']
    ordering = ['question', 'order']

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['test', 'student_name', 'student_class', 'score', 'percentage', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'test__category', 'started_at']
    search_fields = ['student_name', 'student_class']
    ordering = ['-started_at']
    readonly_fields = ['started_at', 'completed_at']

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'attempt__test__category']
    ordering = ['attempt', 'question']
