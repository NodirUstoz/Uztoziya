from rest_framework import serializers
from .models import OCRProcessing, TestResult, ExcelExport


class OCRProcessingSerializer(serializers.ModelSerializer):
    """OCR qayta ishlash serializeri"""
    
    user_name = serializers.SerializerMethodField()
    test_title = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OCRProcessing
        fields = [
            'id', 'user', 'user_name', 'test', 'test_title',
            'image', 'image_url', 'processed_text', 'confidence_score',
            'status', 'status_display', 'error_message', 'processing_time',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']
    
    def get_user_name(self, obj):
        """Foydalanuvchi nomini qaytaradi"""
        return obj.user.get_full_name()
    
    def get_test_title(self, obj):
        """Test sarlavhasini qaytaradi"""
        return obj.test.title if obj.test else None
    
    def get_image_url(self, obj):
        """Rasm URL ini qaytaradi"""
        if obj.image:
            return obj.image.url
        return None
    
    def get_status_display(self, obj):
        """Holat nomini qaytaradi"""
        return obj.get_status_display()


class TestResultSerializer(serializers.ModelSerializer):
    """Test natijasi serializeri"""
    
    student_name = serializers.CharField(read_only=True)
    test_title = serializers.SerializerMethodField()
    grade_display = serializers.SerializerMethodField()
    
    class Meta:
        model = TestResult
        fields = [
            'id', 'ocr_processing', 'student_name', 'student_class',
            'total_questions', 'correct_answers', 'wrong_answers',
            'score', 'percentage', 'grade', 'grade_display',
            'processed_at', 'test_title'
        ]
        read_only_fields = ['id', 'processed_at']
    
    def get_test_title(self, obj):
        """Test sarlavhasini qaytaradi"""
        return obj.ocr_processing.test.title if obj.ocr_processing.test else None
    
    def get_grade_display(self, obj):
        """Baholash nomini qaytaradi"""
        return obj.grade


class ExcelExportSerializer(serializers.ModelSerializer):
    """Excel eksport serializeri"""
    
    user_name = serializers.SerializerMethodField()
    test_title = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = ExcelExport
        fields = [
            'id', 'user', 'user_name', 'test', 'test_title',
            'file', 'file_url', 'file_size', 'total_students',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_name(self, obj):
        """Foydalanuvchi nomini qaytaradi"""
        return obj.user.get_full_name()
    
    def get_test_title(self, obj):
        """Test sarlavhasini qaytaradi"""
        return obj.test.title
    
    def get_file_url(self, obj):
        """Fayl URL ini qaytaradi"""
        if obj.file:
            return obj.file.url
        return None
    
    def get_file_size(self, obj):
        """Fayl hajmini qaytaradi"""
        if obj.file:
            try:
                return obj.file.size
            except:
                return None
        return None
