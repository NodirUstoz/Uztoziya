from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from accounts.models import User
from materials.models import Material, Assignment, VideoLesson, Model3D
from tests.models import Test, Question, Answer, TestCategory
from ocr_processing.models import OCRProcessing


def home(request):
    """Asosiy sahifa"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Statistikalar
    total_materials = Material.objects.filter(is_public=True).count()
    total_tests = Test.objects.filter(is_public=True, is_active=True).count()
    total_users = User.objects.filter(is_active=True).count()
    
    context = {
        'total_materials': total_materials,
        'total_tests': total_tests,
        'total_users': total_users,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """Dashboard sahifasi"""
    user = request.user
    
    # Statistikalar
    materials_count = Material.objects.filter(author=user).count()
    tests_count = Test.objects.filter(author=user).count()
    assignments_count = Assignment.objects.filter(teacher=user).count()
    videos_count = VideoLesson.objects.filter(author=user).count()
    models_3d_count = Model3D.objects.filter(author=user).count()
    ocr_count = OCRProcessing.objects.filter(user=user).count()
    
    # So'nggi materiallar
    recent_materials = Material.objects.filter(author=user).order_by('-created_at')[:5]
    
    # So'nggi testlar - barcha testlarni ko'rsatish (umumiy foydalanish uchun)
    recent_tests = Test.objects.filter(is_public=True, is_active=True).order_by('-created_at')[:5]
    
    context = {
        'stats': {
            'materials_count': materials_count,
            'tests_count': tests_count,
            'assignments_count': assignments_count,
            'videos_count': videos_count,
            'models_3d_count': models_3d_count,
            'ocr_count': ocr_count,
        },
        'recent_materials': recent_materials,
        'recent_tests': recent_tests,
    }
    return render(request, 'dashboard.html', context)


def register_view(request):
    """Ro'yxatdan o'tish sahifasi"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        subject = request.POST.get('subject')
        school = request.POST.get('school')
        phone = request.POST.get('phone')
        
        if password != password_confirm:
            messages.error(request, 'Parollar mos kelmaydi')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu foydalanuvchi nomi allaqachon mavjud')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu email allaqachon mavjud')
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                subject=subject,
                school=school,
                phone=phone
            )
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return render(request, 'register.html')


def login_view(request):
    """Kirish sahifasi"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli kirdingiz!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Noto\'g\'ri foydalanuvchi nomi yoki parol')
    
    return render(request, 'login.html')


def logout_view(request):
    """Chiqish"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Muvaffaqiyatli chiqdingiz!')
    return redirect('home')


@login_required
def profile(request):
    """Profil sahifasi"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.subject = request.POST.get('subject', user.subject)
        user.school = request.POST.get('school', user.school)
        user.phone = request.POST.get('phone', user.phone)
        user.bio = request.POST.get('bio', user.bio)
        
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
        return redirect('profile')
    
    return render(request, 'profile.html')


@login_required
def materials_list(request):
    """Materiallar ro'yxati"""
    materials = Material.objects.filter(is_public=True).order_by('-created_at')
    
    # Filtrlash
    category = request.GET.get('category')
    material_type = request.GET.get('type')
    subject = request.GET.get('subject')
    search = request.GET.get('search')
    
    if category:
        materials = materials.filter(category_id=category)
    if material_type:
        materials = materials.filter(material_type=material_type)
    if subject:
        materials = materials.filter(author__subject=subject)
    if search:
        materials = materials.filter(
            title__icontains=search
        )
    
    context = {
        'materials': materials,
    }
    return render(request, 'materials/list.html', context)


@login_required
def material_create(request):
    """Yangi material yaratish"""
    if request.method == 'POST':
        try:
            from materials.models import MaterialCategory
            
            # Kategoriyani olish yoki yaratish
            category_id = request.POST.get('category')
            if category_id:
                category = MaterialCategory.objects.get(id=category_id)
            else:
                # Agar kategoriya tanlanmagan bo'lsa, default kategoriya yaratamiz
                category, created = MaterialCategory.objects.get_or_create(
                    name='Umumiy',
                    defaults={'description': 'Umumiy materiallar'}
                )
            
            # Material yaratish
            material = Material.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                material_type=request.POST.get('material_type'),
                category=category,
                grade_level=request.POST.get('grade_level', ''),
                tags=request.POST.get('tags', ''),
                is_public=request.POST.get('is_public') == 'on',
                author=request.user,
                file=request.FILES.get('file')
            )
            
            # Kichik rasm qo'shish
            if 'thumbnail' in request.FILES:
                material.thumbnail = request.FILES['thumbnail']
                material.save()
            
            messages.success(request, 'Material muvaffaqiyatli yaratildi!')
            return redirect('materials_list')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return render(request, 'materials/create.html')
    
    # Kategoriyalarni olish
    from materials.models import MaterialCategory
    categories = MaterialCategory.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'materials/create.html', context)


@login_required
def tests_list(request):
    """Testlar ro'yxati"""
    tests = Test.objects.filter(is_public=True, is_active=True).order_by('-created_at')
    
    # Filtrlash
    category = request.GET.get('category')
    subject = request.GET.get('subject')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if category:
        tests = tests.filter(category_id=category)
    if subject:
        tests = tests.filter(subject=subject)
    if difficulty:
        tests = tests.filter(difficulty=difficulty)
    if search:
        tests = tests.filter(title__icontains=search)
    
    context = {
        'tests': tests,
    }
    return render(request, 'tests/list.html', context)


@login_required
def test_create(request):
    """Yangi test yaratish"""
    if request.method == 'POST':
        try:
            # Kategoriyani olish yoki yaratish
            category_id = request.POST.get('category')
            if category_id:
                category = TestCategory.objects.get(id=category_id)
            else:
                # Agar kategoriya tanlanmagan bo'lsa, default kategoriya yaratamiz
                category, created = TestCategory.objects.get_or_create(
                    name='Umumiy',
                    defaults={'description': 'Umumiy testlar'}
                )
            
            # Test yaratish
            test = Test.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                category=category,
                subject=request.POST.get('subject', 'Umumiy'),
                grade_level=request.POST.get('grade_level', 'Barcha sinflar'),
                difficulty=request.POST.get('difficulty', 'medium'),
                time_limit=int(request.POST.get('time_limit', 60)),
                is_public=request.POST.get('is_public') == 'true',
                author=request.user
            )
            
            # Savollar yaratish
            questions_data = request.POST.get('questions', '[]')
            if questions_data:
                import json
                questions = json.loads(questions_data)
                
                for i, question_data in enumerate(questions):
                    question = Question.objects.create(
                        test=test,
                        question_text=question_data.get('text'),
                        question_type=question_data.get('type'),
                        points=int(question_data.get('points', 1)),
                        order=i + 1,
                        explanation=question_data.get('explanation', '')
                    )
                    
                    # Javoblar yaratish
                    for j, answer_data in enumerate(question_data.get('answers', [])):
                        Answer.objects.create(
                            question=question,
                            answer_text=answer_data.get('text'),
                            is_correct=answer_data.get('is_correct', False),
                            order=j + 1
                        )
            
            # Test statistikasini yangilash
            test.total_questions = test.questions.count()
            test.total_points = sum(q.points for q in test.questions.all())
            test.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Test muvaffaqiyatli yaratildi!',
                'test_id': test.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Xatolik yuz berdi: {str(e)}'
            })
    
    # Kategoriyalarni olish
    categories = TestCategory.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'tests/create.html', context)


@login_required
def ocr_upload(request):
    """OCR rasm yuklash sahifasi"""
    tests = Test.objects.filter(author=request.user, is_active=True)
    
    context = {
        'tests': tests,
    }
    return render(request, 'ocr_upload.html', context)


@login_required
def assignments_list(request):
    """Topshiriqlar ro'yxati"""
    return render(request, 'assignments/list.html')


@login_required
def videos_list(request):
    """Video darsliklar ro'yxati"""
    return render(request, 'videos/list.html')


@login_required
def models_3d_list(request):
    """3D modellar ro'yxati"""
    return render(request, '3d_models/list.html')
