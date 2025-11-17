from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.material_ai_categories, name='categories'),
    path('presentation/', views.material_presentation_view, name='presentation'),
    path('interactive/', views.material_interactive_view, name='interactive'),
    path('image/', views.material_image_view, name='image'),
    path('resources/', views.material_resources_view, name='resources'),
]
