from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register_api'),
    path('login/', views.login_view, name='login_api'),
    path('logout/', views.logout_view, name='logout_api'),
    path('profile/', views.profile, name='profile_api'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('users/', views.UserListView.as_view(), name='user_list'),
]
