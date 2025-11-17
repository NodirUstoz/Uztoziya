import google.generativeai as genai
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class AITestGenerationService:
    """AI yordamida test yaratish xizmati - Google Gemini API"""
    
    def __init__(self):
        # Google Gemini API'ni sozlash
        try:
            genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')  # gemini-pro yoki gemini-1.5-pro
        except Exception as e:
            logger.error(f"Gemini API sozlashda xatolik: {e}")
            self.model = None
    
    def generate_test_questions(self, subject, grade_level, difficulty, num_questions=5, language='uzbek'):
        """AI yordamida test savollarini yaratish"""
        try:
            # Agar model mavjud bo'lmasa, mock data qaytarish
            if not self.model:
                logger.warning("Gemini model mavjud emas, mock data qaytarilmoqda")
                return self._generate_mock_questions(subject, grade_level, difficulty, num_questions)
            
            # Agar API key test bo'lsa, mock data qaytarish
            if settings.GOOGLE_GEMINI_API_KEY in ['YOUR_API_KEY_HERE', 'AIzaSyA7hPIidsVobpDQPGxPXb46yvEQhIMDzOo']:
                logger.warning("Demo API key ishlatilmoqda, mock data qaytarilmoqda")
                return self._generate_mock_questions(subject, grade_level, difficulty, num_questions)
            
            # Prompt yaratish
            prompt = self._create_prompt(subject, grade_level, difficulty, num_questions, language)
            
            # Gemini'ga so'rov yuborish
            logger.info(f"Gemini'ga so'rov yuborilmoqda: {subject}, {grade_level}, {difficulty}")
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # JSON formatda parse qilish
            questions = self._parse_ai_response(response_text)
            
            if questions:
                return questions
            else:
                logger.warning("AI javobini parse qila olmadi, mock data qaytarilmoqda")
                return self._generate_mock_questions(subject, grade_level, difficulty, num_questions)
            
        except Exception as e:
            logger.error(f"AI test generation xatoligi: {e}")
            # Xatolik bo'lsa, mock data qaytarish
            return self._generate_mock_questions(subject, grade_level, difficulty, num_questions)
    
    def _create_prompt(self, subject, grade_level, difficulty, num_questions, language):
        """AI uchun prompt yaratish - o'rta darajadagi savollar uchun optimallashtirilgan"""
        
        difficulty_map = {
            'easy': 'oson',
            'medium': 'o\'rta',
            'hard': 'qiyin'
        }
        
        difficulty_text = difficulty_map.get(difficulty, 'o\'rta')
        
        # Fan nomini o'zbekchaga o'girish
        subject_map = {
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
            'physical_education': 'Jismoniy tarbiya'
        }
        
        subject_uz = subject_map.get(subject.lower(), subject)
        
        prompt = f"""Siz {subject_uz} fanidan {grade_level}-sinf uchun {difficulty_text} darajadagi {num_questions} ta test savoli yaratishingiz kerak.

MAJBURIY TALABLAR:
1. Savollar o'rta darajada bo'lishi kerak - oddiy emas, lekin juda qiyin ham emas
2. Har bir savol real hayotiy stsenariy yoki amaliy masala bo'lishi kerak
3. Savollar mantiqiy fikrlashni talab qilishi kerak
4. Har bir savol uchun aniq va to'g'ri tushuntirish bo'lishi kerak
5. Savollar {grade_level}-sinf darajasiga mos bo'lishi kerak

FORMAT (faqat JSON kod qaytaring):
{{
    "questions": [
        {{
            "question_text": "Savol matni o'zbek tilida",
            "question_type": "single_choice",
            "points": 1,
            "explanation": "To'g'ri javob uchun tushuntirish",
            "answers": [
                {{"answer_text": "A) Birinchi variant", "is_correct": true}},
                {{"answer_text": "B) Ikkinchi variant", "is_correct": false}},
                {{"answer_text": "C) Uchinchi variant", "is_correct": false}},
                {{"answer_text": "D) To'rtinchi variant", "is_correct": false}}
            ]
        }}
    ]
}}

QO'SHIMCHA QOIDALAR:
- Faqat JSON format qaytaring, boshqa matn qo'shmang
- Har bir savol uchun bitta to'g'ri javob
- Har bir savol uchun 4 ta javob variant
- Savollar o'zbek tilida
- Tushuntirishlar aniq va foydali bo'lishi kerak
- {subject_uz} faniga tegishli mavzular
- {difficulty_text} darajadagi murakkablik"""
        
        return prompt
    
    def _parse_ai_response(self, response_text):
        """AI javobini parse qilish - yaxshilangan"""
        try:
            # JSON qismini ajratib olish
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("JSON format topilmadi")
                return None
            
            json_text = response_text[start_idx:end_idx]
            logger.info(f"Parsing JSON: {json_text[:200]}...")
            
            data = json.loads(json_text)
            questions = data.get('questions', [])
            
            # Savollar sonini tekshirish
            if not questions:
                logger.error("Savollar topilmadi")
                return None
                
            logger.info(f"Muvaffaqiyatli parse qilindi: {len(questions)} ta savol")
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse xatoligi: {e}")
            logger.error(f"Response text: {response_text}")
            return None
        except Exception as e:
            logger.error(f"AI javobini qayta ishlashda xatolik: {e}")
            return None
    
    def generate_test_title(self, subject, grade_level, difficulty, topic=None):
        """AI yordamida test sarlavhasi yaratish"""
        try:
            # Fan nomini o'zbekchaga o'girish
            subject_map = {
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
                'physical_education': 'Jismoniy tarbiya'
            }
            
            subject_uz = subject_map.get(subject.lower(), subject)
            
            prompt = f"""
{subject_uz} fanidan {grade_level}-sinf uchun {difficulty} darajadagi test uchun qisqa va jozibali sarlavha yarating.
{f"Test mavzusi: {topic}" if topic else ""}

Sarlavha talablari:
- Qisqa va aniq bo'lishi kerak (maksimal 50 ta harf)
- O'zbek tilida bo'lishi kerak
- {grade_level}-sinf darajasiga mos bo'lishi kerak
- Jozibali va motivatsiyalovchi bo'lishi kerak
- Faqat sarlavha matnini qaytaring, boshqa matn qo'shmang
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"AI test title generation xatoligi: {e}")
            return f"{subject_uz} testi ({grade_level}-sinf)"
    
    def generate_test_description(self, subject, grade_level, difficulty, questions_count):
        """AI yordamida test tavsifini yaratish"""
        try:
            # Fan nomini o'zbekchaga o'girish
            subject_map = {
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
                'physical_education': 'Jismoniy tarbiya'
            }
            
            subject_uz = subject_map.get(subject.lower(), subject)
            
            prompt = f"""
{subject_uz} fanidan {grade_level}-sinf uchun {difficulty} darajadagi {questions_count} ta savolli test uchun qisqa tavsif yarating.

Tavsif talablari:
- Qisqa va aniq bo'lishi kerak (maksimal 100 ta harf)
- O'zbek tilida bo'lishi kerak
- Test haqida umumiy ma'lumot berishi kerak
- O'quvchilarni test topshirishga undovchi bo'lishi kerak
- Faqat tavsif matnini qaytaring, boshqa matn qo'shmang
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"AI test description generation xatoligi: {e}")
            return f"{subject_uz} fanidan {grade_level}-sinf uchun {questions_count} ta savolli test"
    
    def _generate_mock_questions(self, subject, grade_level, difficulty, num_questions):
        """Test uchun mock savollar yaratish - yaxshilangan"""
        
        # Fan nomini o'zbekchaga o'girish
        subject_map = {
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
            'physical_education': 'Jismoniy tarbiya'
        }
        
        subject_uz = subject_map.get(subject.lower(), subject)
        questions = []
        
        for i in range(num_questions):
            question = {
                "question_text": f"{subject_uz} fanidan {grade_level}-sinf uchun {i+1}-savol: Bu {difficulty} darajadagi test savoli hisoblanadi. Savol matnini bu yerda ko'rsating.",
                "question_type": "single_choice",
                "points": 1,
                "explanation": f"Bu {subject_uz} fanidan {grade_level}-sinf uchun {difficulty} darajadagi savol uchun tushuntirish.",
                "answers": [
                    {
                        "answer_text": "A) To'g'ri javob",
                        "is_correct": True
                    },
                    {
                        "answer_text": "B) Noto'g'ri javob",
                        "is_correct": False
                    },
                    {
                        "answer_text": "C) Noto'g'ri javob",
                        "is_correct": False
                    },
                    {
                        "answer_text": "D) Noto'g'ri javob",
                        "is_correct": False
                    }
                ]
            }
            questions.append(question)
        
        return questions
