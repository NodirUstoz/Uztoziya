from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer
)


def login_required_view(request):
    """Login required sahifasi"""
    return render(request, 'login.html')


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    """Foydalanuvchi ro'yxatdan o'tish"""
    if request.method == 'GET':
        return render(request, 'register.html')
    
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Muvaffaqiyatli ro\'yxatdan o\'tildi',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Foydalanuvchi kirish"""
    if request.method == 'GET':
        return render(request, 'login.html')
    
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Muvaffaqiyatli kirdingiz',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Foydalanuvchi chiqish"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    return Response({
        'message': 'Muvaffaqiyatli chiqdingiz'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Foydalanuvchi profili"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Foydalanuvchi ma'lumotlarini yangilash"""
    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profil muvaffaqiyatli yangilandi',
            'user': UserProfileSerializer(request.user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Parol o'zgartirish"""
    serializer = PasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Parol muvaffaqiyatli o\'zgartirildi'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Dashboard statistikasi"""
    user = request.user
    
    # Materiallar soni
    materials_count = user.materials.count()
    
    # Testlar soni
    tests_count = user.tests.count()
    
    # OCR qayta ishlashlar soni
    ocr_count = user.ocr_processings.count()
    
    # Excel eksportlar soni
    excel_count = user.excel_exports.count()
    
    return Response({
        'materials_count': materials_count,
        'tests_count': tests_count,
        'ocr_count': ocr_count,
        'excel_count': excel_count
    })


class UserListView(generics.ListAPIView):
    """Foydalanuvchilar ro'yxati (faqat admin)"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Faqat admin barcha foydalanuvchilarni ko'ra oladi
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)