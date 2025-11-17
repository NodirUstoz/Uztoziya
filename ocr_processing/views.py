from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os
import logging

from .models import OCRProcessing, TestResult, ExcelExport
from .services import OCRService
from tests.models import Test
from .serializers import (
    OCRProcessingSerializer,
    TestResultSerializer,
    ExcelExportSerializer
)

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_test_image(request):
    """Test rasmini yuklash va OCR qilish"""
    try:
        if 'image' not in request.FILES:
            return Response({
                'error': 'Rasm fayli yuklanmagan'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        test_id = request.data.get('test_id')
        
        # OCR qayta ishlash obyektini yaratish
        ocr_processing = OCRProcessing.objects.create(
            user=request.user,
            image=image_file,
            status='pending'
        )
        
        if test_id:
            try:
                test = Test.objects.get(id=test_id, author=request.user)
                ocr_processing.test = test
                ocr_processing.save()
            except Test.DoesNotExist:
                return Response({
                    'error': 'Test topilmadi'
                }, status=status.HTTP_404_NOT_FOUND)
        
        # OCR qilish - Google Vision API va Tesseract
        ocr_service = OCRService()
        text, confidence = ocr_service.extract_text(ocr_processing.image.path)
        
        if text:
            ocr_processing.processed_text = text
            ocr_processing.confidence_score = confidence
            ocr_processing.status = 'completed'
        else:
            ocr_processing.status = 'failed'
            ocr_processing.error_message = 'Matn ajratib olinmadi'
        
        ocr_processing.save()
        
        # Agar test belgilangan bo'lsa, baholash (vaqtincha o'chirilgan)
        test_result = None
        if test_id and ocr_processing.status == 'completed':
            # grading_service = TestGradingService()
            # test_result = grading_service.grade_test(ocr_processing, test)
            pass
            
            if test_result:
                return Response({
                    'message': 'Test muvaffaqiyatli qayta ishlandi va baholandi',
                    'ocr_processing': OCRProcessingSerializer(ocr_processing).data,
                    'test_result': TestResultSerializer(test_result).data
                })
        
        return Response({
            'message': 'Rasm muvaffaqiyatli qayta ishlandi',
            'ocr_processing': OCRProcessingSerializer(ocr_processing).data
        })
        
    except Exception as e:
        logger.error(f"OCR qayta ishlashda xatolik: {e}")
        return Response({
            'error': 'Server xatoligi yuz berdi'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ocr_processing_list(request):
    """OCR qayta ishlashlar ro'yxati"""
    processings = OCRProcessing.objects.filter(user=request.user).order_by('-created_at')
    serializer = OCRProcessingSerializer(processings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ocr_processing_detail(request, pk):
    """OCR qayta ishlash tafsilotlari"""
    processing = get_object_or_404(OCRProcessing, pk=pk, user=request.user)
    serializer = OCRProcessingSerializer(processing)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_results_list(request, test_id):
    """Test natijalari ro'yxati"""
    test = get_object_or_404(Test, pk=test_id, author=request.user)
    results = TestResult.objects.filter(ocr_processing__test=test).order_by('-processed_at')
    serializer = TestResultSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_to_excel(request, test_id):
    """Test natijalarini Excel ga eksport qilish"""
    try:
        test = get_object_or_404(Test, pk=test_id, author=request.user)
        results = TestResult.objects.filter(ocr_processing__test=test)
        
        if not results.exists():
            return Response({
                'error': 'Eksport qilish uchun natijalar mavjud emas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Excel fayl yaratish (vaqtincha o'chirilgan)
        excel_path = None
        # excel_service = ExcelExportService()
        # excel_path = excel_service.export_test_results(test, list(results))
        
        if not excel_path:
            return Response({
                'error': 'Excel fayl yaratishda xatolik'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Excel eksport obyektini yaratish
        excel_export = ExcelExport.objects.create(
            user=request.user,
            test=test,
            file=excel_path,
            total_students=results.count()
        )
        
        return Response({
            'message': 'Excel fayl muvaffaqiyatli yaratildi',
            'excel_export': ExcelExportSerializer(excel_export).data,
            'download_url': excel_export.file.url
        })
        
    except Exception as e:
        logger.error(f"Excel eksportda xatolik: {e}")
        return Response({
            'error': 'Server xatoligi yuz berdi'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_excel(request, export_id):
    """Excel faylini yuklab olish"""
    try:
        excel_export = get_object_or_404(ExcelExport, pk=export_id, user=request.user)
        
        if not os.path.exists(excel_export.file.path):
            return Response({
                'error': 'Fayl topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)
        
        with open(excel_export.file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="test_results_{excel_export.test.id}.xlsx"'
            return response
            
    except Exception as e:
        logger.error(f"Excel yuklab olishda xatolik: {e}")
        return Response({
            'error': 'Server xatoligi yuz berdi'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def excel_exports_list(request):
    """Excel eksportlar ro'yxati"""
    exports = ExcelExport.objects.filter(user=request.user).order_by('-created_at')
    serializer = ExcelExportSerializer(exports, many=True)
    return Response(serializer.data)


class OCRProcessingListView(generics.ListAPIView):
    """OCR qayta ishlashlar ro'yxati (Generic View)"""
    serializer_class = OCRProcessingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return OCRProcessing.objects.filter(user=self.request.user).order_by('-created_at')


class TestResultListView(generics.ListAPIView):
    """Test natijalari ro'yxati (Generic View)"""
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        test_id = self.kwargs.get('test_id')
        if test_id:
            return TestResult.objects.filter(
                ocr_processing__test_id=test_id,
                ocr_processing__user=self.request.user
            ).order_by('-processed_at')
        return TestResult.objects.filter(
            ocr_processing__user=self.request.user
        ).order_by('-processed_at')