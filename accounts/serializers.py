from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Foydalanuvchi ro'yxatdan o'tish serializeri"""
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'role', 'subject',
            'school', 'phone', 'bio'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
    
    def validate(self, attrs):
        """Parolni tekshirish"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Parollar mos kelmaydi")
        return attrs
    
    def create(self, validated_data):
        """Yangi foydalanuvchi yaratish"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Foydalanuvchi kirish serializeri"""
    
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        """Kirish ma'lumotlarini tekshirish"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Noto\'g\'ri foydalanuvchi nomi yoki parol'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Foydalanuvchi hisobi faol emas'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Foydalanuvchi nomi va parol kiritilishi kerak'
            )


class UserProfileSerializer(serializers.ModelSerializer):
    """Foydalanuvchi profil serializeri"""
    
    full_name = serializers.SerializerMethodField()
    subject_display = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'role_display', 'subject', 'subject_display',
            'school', 'phone', 'avatar', 'bio', 'is_verified',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        """To'liq ismni qaytaradi"""
        return obj.get_full_name()
    
    def get_subject_display(self, obj):
        """Fan nomini qaytaradi"""
        return obj.get_subject_display()
    
    def get_role_display(self, obj):
        """Rol nomini qaytaradi"""
        return obj.get_role_display()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Foydalanuvchi ma'lumotlarini yangilash serializeri"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'subject',
            'school', 'phone', 'avatar', 'bio'
        ]
    
    def validate_email(self, value):
        """Email unikalligini tekshirish"""
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Bu email allaqachon ishlatilgan")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """Parol o'zgartirish serializeri"""
    
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        validators=[validate_password],
        style={'input_type': 'password'},
        write_only=True
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        """Parolni tekshirish"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Yangi parollar mos kelmaydi")
        return attrs
    
    def validate_old_password(self, value):
        """Eski parolni tekshirish"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto'g'ri")
        return value
    
    def save(self):
        """Yangi parolni saqlash"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
