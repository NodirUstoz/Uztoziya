from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_test_image, name='upload_test_image'),
    path('processings/', views.ocr_processing_list, name='ocr_processing_list'),
    path('processings/<int:pk>/', views.ocr_processing_detail, name='ocr_processing_detail'),
    path('test-results/<int:test_id>/', views.test_results_list, name='test_results_list'),
    path('export-excel/<int:test_id>/', views.export_to_excel, name='export_to_excel'),
    path('download-excel/<int:export_id>/', views.download_excel, name='download_excel'),
    path('excel-exports/', views.excel_exports_list, name='excel_exports_list'),
]
