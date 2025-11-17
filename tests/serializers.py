from rest_framework import serializers
from .models import Test, Question, Answer, TestAttempt, StudentAnswer, TestCategory


class TestCategorySerializer(serializers.ModelSerializer):
    """Test kategoriya serializeri"""
    
    tests_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TestCategory
        fields = ['id', 'name', 'description', 'tests_count']
    
    def get_tests_count(self, obj):
        """Kategoriyadagi testlar soni"""
        return obj.tests.filter(is_public=True, is_active=True).count()


class AnswerSerializer(serializers.ModelSerializer):
    """Javob serializeri"""
    
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Savol serializeri"""
    
    answers = AnswerSerializer(many=True, read_only=True)
    test_title = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    question_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'test', 'test_title', 'question_text', 'question_type',
            'question_type_display', 'points', 'order', 'explanation',
            'image', 'image_url', 'answers', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_test_title(self, obj):
        """Test sarlavhasini qaytaradi"""
        return obj.test.title
    
    def get_image_url(self, obj):
        """Savol rasmi URL ini qaytaradi"""
        if obj.image:
            return obj.image.url
        return None
    
    def get_question_type_display(self, obj):
        """Savol turi nomini qaytaradi"""
        return obj.get_question_type_display()


class TestSerializer(serializers.ModelSerializer):
    """Test serializeri"""
    
    author_name = serializers.SerializerMethodField()
    author_subject = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    subject_display = serializers.SerializerMethodField()
    difficulty_display = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    attempts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'author', 'author_name', 'author_subject', 'difficulty',
            'difficulty_display', 'grade_level', 'subject', 'subject_display',
            'time_limit', 'total_questions', 'total_points', 'is_public',
            'is_active', 'questions_count', 'attempts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'total_questions', 'total_points', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        """Muallif nomini qaytaradi"""
        return obj.author.get_full_name()
    
    def get_author_subject(self, obj):
        """Muallif fanini qaytaradi"""
        return obj.author.get_subject_display()
    
    def get_category_name(self, obj):
        """Kategoriya nomini qaytaradi"""
        return obj.category.name if obj.category else None
    
    def get_subject_display(self, obj):
        """Fan nomini qaytaradi"""
        # Subject field mapping
        subject_choices = {
            'mathematics': 'Matematika',
            'physics': 'Fizika',
            'chemistry': 'Kimyo',
            'biology': 'Biologiya',
            'geography': 'Geografiya',
            'history': 'Tarix',
            'literature': 'Adabiyot',
            'language': 'Til va adabiyot',
            'english': 'Ingliz tili',
            'russian': 'Rus tili',
            'computer_science': 'Informatika',
            'art': 'San\'at',
            'physical_education': 'Jismoniy tarbiya',
            'other': 'Boshqa'
        }
        return subject_choices.get(obj.subject, obj.subject)
    
    def get_difficulty_display(self, obj):
        """Qiyinlik darajasi nomini qaytaradi"""
        return obj.get_difficulty_display()
    
    def get_questions_count(self, obj):
        """Savollar soni"""
        return obj.questions.count()
    
    def get_attempts_count(self, obj):
        """Topshirishlar soni"""
        return obj.attempts.count()


class StudentAnswerSerializer(serializers.ModelSerializer):
    """O'quvchi javob serializeri"""
    
    question_text = serializers.SerializerMethodField()
    selected_answers_text = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentAnswer
        fields = [
            'id', 'attempt', 'question', 'question_text', 'selected_answers',
            'selected_answers_text', 'text_answer', 'is_correct', 'points_earned',
            'answered_at'
        ]
        read_only_fields = ['id', 'answered_at']
    
    def get_question_text(self, obj):
        """Savol matnini qaytaradi"""
        return obj.question.question_text
    
    def get_selected_answers_text(self, obj):
        """Tanlangan javoblar matnini qaytaradi"""
        return [answer.answer_text for answer in obj.selected_answers.all()]


class TestAttemptSerializer(serializers.ModelSerializer):
    """Test topshirish serializeri"""
    
    test_title = serializers.SerializerMethodField()
    student_answers = StudentAnswerSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = TestAttempt
        fields = [
            'id', 'test', 'test_title', 'student_name', 'student_class',
            'started_at', 'completed_at', 'duration', 'score', 'percentage',
            'is_completed', 'student_answers'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'duration']
    
    def get_test_title(self, obj):
        """Test sarlavhasini qaytaradi"""
        return obj.test.title
    
    def get_duration(self, obj):
        """Test davomiyligini qaytaradi"""
        if obj.completed_at and obj.started_at:
            duration = obj.completed_at - obj.started_at
            return duration.total_seconds() / 60  # daqiqalarda
        return None


class TestCreateSerializer(serializers.ModelSerializer):
    """Test yaratish serializeri"""
    
    class Meta:
        model = Test
        fields = [
            'title', 'description', 'category', 'difficulty', 'grade_level',
            'subject', 'time_limit', 'is_public', 'is_active'
        ]
    
    def validate_time_limit(self, value):
        """Vaqt chegarasini tekshirish"""
        if value <= 0:
            raise serializers.ValidationError("Vaqt chegarasi 0 dan katta bo'lishi kerak")
        return value


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Savol yaratish serializeri"""
    
    answers = AnswerSerializer(many=True, write_only=True)
    
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'points', 'order',
            'explanation', 'image', 'answers'
        ]
    
    def create(self, validated_data):
        """Savol va javoblarini yaratish"""
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        
        return question
    
    def update(self, instance, validated_data):
        """Savol va javoblarini yangilash"""
        answers_data = validated_data.pop('answers', None)
        
        # Savolni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Javoblarni yangilash
        if answers_data is not None:
            # Eski javoblarni o'chirish
            instance.answers.all().delete()
            
            # Yangi javoblarni yaratish
            for answer_data in answers_data:
                Answer.objects.create(question=instance, **answer_data)
        
        return instance
