from django.urls import path
from . import views

urlpatterns = [
    # Material categories (API)
    path('categories/', views.MaterialCategoryListView.as_view(), name='material_category_list'),

    # Materials CRUD (API)
    path('', views.MaterialListView.as_view(), name='material_list'),
    path('create/', views.MaterialCreateView.as_view(), name='material_create'),
    path('<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('<int:pk>/update/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
    path('<int:pk>/download/', views.download_material, name='material_download'),
    path('<int:pk>/rate/', views.rate_material, name='material_rate'),
    path('search/', views.search_materials, name='search_materials'),
    path('my-materials/', views.my_materials, name='my_materials'),
    path('stats/', views.material_stats, name='material_stats'),

    # Assignments (API)
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),

    # Student submissions (API)
    path('submissions/', views.StudentSubmissionListView.as_view(), name='submission_list'),
    path('submissions/<int:pk>/', views.StudentSubmissionDetailView.as_view(), name='submission_detail'),
    path('submissions/<int:pk>/grade/', views.grade_submission, name='grade_submission'),

    # Video lessons (API)
    path('videos/', views.VideoLessonListView.as_view(), name='video_lesson_list'),
    path('videos/<int:pk>/', views.VideoLessonDetailView.as_view(), name='video_lesson_detail'),
    path('videos/<int:pk>/watch/', views.watch_video, name='watch_video'),

    # 3D Models (API)
    path('3d-models/', views.Model3DListView.as_view(), name='model_3d_list'),
    path('3d-models/<int:pk>/', views.Model3DDetailView.as_view(), name='model_3d_detail'),
    path('3d-models/<int:pk>/download/', views.download_3d_model, name='download_3d_model'),
]

