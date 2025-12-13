#!/usr/bin/env python
"""
Script to update translation files with Uzbek and Russian translations
"""

translations = {
    # Language names
    "Uzbek": {"uz": "O'zbekcha", "ru": "Узбекский"},
    "English": {"uz": "Inglizcha", "ru": "Английский"},
    "Russian": {"uz": "Ruscha", "ru": "Русский"},
    
    # Admin
    "Basirat LMS Administration": {"uz": "Basirat LMS Boshqaruvi", "ru": "Администрирование Basirat LMS"},
    "Basirat Admin": {"uz": "Basirat Boshqaruv", "ru": "Basirat Админ"},
    "Learning Management System": {"uz": "Ta'lim Boshqaruv Tizimi", "ru": "Система Управления Обучением"},
    
    # Course/Lesson/Material admin sections
    "Course Information": {"uz": "Kurs Ma'lumotlari", "ru": "Информация о курсе"},
    "Lesson Information": {"uz": "Dars Ma'lumotlari", "ru": "Информация об уроке"},
    "Material Information": {"uz": "Material Ma'lumotlari", "ru": "Информация о материале"},
    "Dates": {"uz": "Sanalar", "ru": "Даты"},
    "Materials": {"uz": "Materiallar", "ru": "Материалы"},
    "Learning Content": {"uz": "O'quv Materiali", "ru": "Учебное содержание"},
    "Task Content": {"uz": "Topshiriq Materiali", "ru": "Содержание задания"},
    "For learning materials only. Leave empty for tasks.": {"uz": "Faqat o'quv materiallari uchun. Topshiriqlar uchun bo'sh qoldiring.", "ru": "Только для учебных материалов. Оставьте пустым для заданий."},
    "For task materials only. Leave empty for learning materials.": {"uz": "Faqat topshiriqlar uchun. O'quv materiallari uchun bo'sh qoldiring.", "ru": "Только для заданий. Оставьте пустым для учебных материалов."},
    "Enrollment Details": {"uz": "Ro'yxatdan O'tish Tafsilotlari", "ru": "Детали регистрации"},
    "Completion Details": {"uz": "Tugatish Tafsilotlari", "ru": "Детали завершения"},
    "Submission Information": {"uz": "Topshiriq Ma'lumotlari", "ru": "Информация о представлении"},
    "Student Answer": {"uz": "Talaba Javobi", "ru": "Ответ студента"},
    "The answer submitted by the student": {"uz": "Talaba topshirgan javob", "ru": "Ответ, представленный студентом"},
    "Grading": {"uz": "Baholash", "ru": "Оценивание"},
    "Enter score (0-100) and feedback, then use actions to mark as graded": {"uz": "Ball (0-100) va fikrni kiriting, so'ng baholangan deb belgilash uchun amallardan foydalaning", "ru": "Введите оценку (0-100) и отзыв, затем используйте действия для пометки как оцененного"},
    
    # Admin list displays
    "Student Name": {"uz": "Talaba Ismi", "ru": "Имя студента"},
    "Phone Number": {"uz": "Telefon Raqami", "ru": "Номер телефона"},
    "Phone": {"uz": "Telefon", "ru": "Телефон"},
    "Lesson": {"uz": "Dars", "ru": "Урок"},
    "Question Type": {"uz": "Savol Turi", "ru": "Тип вопроса"},
    
    # Admin actions
    "Mark as graded if score set": {"uz": "Agar ball belgilangan bo'lsa, baholangan deb belgilash", "ru": "Отметить как оцененное, если установлена оценка"},
    "Mark as 100 percent passing": {"uz": "100 foiz o'tgan deb belgilash", "ru": "Отметить как пройденное на 100%"},
    "{count} submissions marked as graded": {"uz": "{count} ta topshiriq baholangan deb belgilandi", "ru": "{count} представлений отмечено как оцененное"},
    "{count} submissions marked as passing": {"uz": "{count} ta topshiriq o'tgan deb belgilandi", "ru": "{count} представлений отмечено как пройденное"},
    "{count} enrollments accepted": {"uz": "{count} ta ro'yxatdan o'tish qabul qilindi", "ru": "{count} регистраций принято"},
    "{count} enrollments rejected": {"uz": "{count} ta ro'yxatdan o'tish rad etildi", "ru": "{count} регистраций отклонено"},
    "Mark selected enrollments as accepted": {"uz": "Tanlangan ro'yxatdan o'tishlarni qabul qilingan deb belgilash", "ru": "Отметить выбранные регистрации как принятые"},
    "Mark selected enrollments as rejected": {"uz": "Tanlangan ro'yxatdan o'tishlarni rad etilgan deb belgilash", "ru": "Отметить выбранные регистрации как отклоненные"},
    
    # Navigation
    "Home": {"uz": "Bosh sahifa", "ru": "Главная"},
    "Dashboard": {"uz": "Boshqaruv Paneli", "ru": "Панель управления"},
    "Submission History": {"uz": "Topshiriqlar Tarixi", "ru": "История представлений"},
    "My Submissions": {"uz": "Mening Topshiriqlarim", "ru": "Мои представления"},
    "Profile": {"uz": "Profil", "ru": "Профиль"},
    "Logout": {"uz": "Chiqish", "ru": "Выход"},
    "Language": {"uz": "Til", "ru": "Язык"},
    
    # Home page
    "Welcome to Basirat": {"uz": "Basirat'ga Xush Kelibsiz", "ru": "Добро пожаловать в Basirat"},
    "Your Learning Journey Starts Here": {"uz": "Sizning O'quv Sayohatingiz Shu Yerdan Boshlanadi", "ru": "Ваше учебное путешествие начинается здесь"},
    "Start Learning": {"uz": "O'qishni Boshlash", "ru": "Начать обучение"},
    "Browse Courses": {"uz": "Kurslarni Ko'rish", "ru": "Просмотр курсов"},
    "Quick Stats": {"uz": "Tezkor Statistika", "ru": "Быстрая статистика"},
    "Active Courses": {"uz": "Faol Kurslar", "ru": "Активные курсы"},
    "Completed Lessons": {"uz": "Tugatilgan Darslar", "ru": "Завершенные уроки"},
    "Total Submissions": {"uz": "Jami Topshiriqlar", "ru": "Всего представлений"},
    "Learning Progress": {"uz": "O'quv Jarayoni", "ru": "Прогресс обучения"},
    "Recent Activity": {"uz": "So'nggi Faoliyat", "ru": "Недавняя активность"},
    "View Full Progress": {"uz": "To'liq Jarayonni Ko'rish", "ru": "Посмотреть полный прогресс"},
    "View History": {"uz": "Tarixni Ko'rish", "ru": "Посмотреть историю"},
    "Featured Courses": {"uz": "Tanlangan Kurslar", "ru": "Избранные курсы"},
    "Get Started": {"uz": "Boshlash", "ru": "Начать"},
    "Continue Learning": {"uz": "O'qishni Davom Ettirish", "ru": "Продолжить обучение"},
    "System Overview": {"uz": "Tizim Sharhi", "ru": "Обзор системы"},
    "Total Courses": {"uz": "Jami Kurslar", "ru": "Всего курсов"},
    "Total Students": {"uz": "Jami Talabalar", "ru": "Всего студентов"},
    "Pending Enrollments": {"uz": "Kutilayotgan Ro'yxatdan O'tishlar", "ru": "Ожидающие регистрации"},
    "Pending Reviews": {"uz": "Kutilayotgan Sharhlar", "ru": "Ожидающие проверки"},
    "Quick Actions": {"uz": "Tezkor Amallar", "ru": "Быстрые действия"},
    "Manage Courses": {"uz": "Kurslarni Boshqarish", "ru": "Управление курсами"},
    "Review Enrollments": {"uz": "Ro'yxatdan O'tishlarni Ko'rib Chiqish", "ru": "Проверка регистраций"},
    "Grade Submissions": {"uz": "Topshiriqlarni Baholash", "ru": "Оценка представлений"},
    "Admin Panel": {"uz": "Boshqaruv Paneli", "ru": "Панель администратора"},
    
    # Courses page
    "Explore available learning paths and start your journey": {"uz": "Mavjud o'quv yo'nalishlarini o'rganing va sayohatingizni boshlang", "ru": "Изучите доступные учебные пути и начните свое путешествие"},
    "Search courses by name or description...": {"uz": "Kurslarni nom yoki tavsif bo'yicha qidirish...", "ru": "Поиск курсов по названию или описанию..."},
    "Sort: A-Z": {"uz": "Tartiblash: A-Z", "ru": "Сортировка: А-Я"},
    "Sort: Z-A": {"uz": "Tartiblash: Z-A", "ru": "Сортировка: Я-А"},
    "Sort: Most Lessons": {"uz": "Tartiblash: Ko'p Darslar", "ru": "Сортировка: Больше уроков"},
    "Search": {"uz": "Qidirish", "ru": "Поиск"},
    "Clear": {"uz": "Tozalash", "ru": "Очистить"},
    "View Course": {"uz": "Kursni Ko'rish", "ru": "Посмотреть курс"},
    "No description available": {"uz": "Tavsif mavjud emas", "ru": "Описание недоступно"},
    "No Courses Found": {"uz": "Kurslar Topilmadi", "ru": "Курсы не найдены"},
    "No Courses Available": {"uz": "Kurslar Mavjud Emas", "ru": "Курсы недоступны"},
    "No courses match your search. Try different keywords or clear the search.": {"uz": "Qidiruvingizga mos kurslar topilmadi. Boshqa kalit so'zlarni sinab ko'ring yoki qidiruvni tozalang.", "ru": "Ни один курс не соответствует вашему поиску. Попробуйте другие ключевые слова или очистите поиск."},
    "Course catalog is empty at the moment. Please check back later.": {"uz": "Kurslar katalogi hozircha bo'sh. Keyinroq qaytib tekshiring.", "ru": "Каталог курсов пуст в данный момент. Пожалуйста, проверьте позже."},
    "View All Courses": {"uz": "Barcha Kurslarni Ko'rish", "ru": "Посмотреть все курсы"},
    
    # Course detail page
    "Enroll in Course": {"uz": "Kursga Yozilish", "ru": "Записаться на курс"},
    "Enrollment Pending": {"uz": "Ro'yxatdan O'tish Kutilmoqda", "ru": "Регистрация ожидается"},
    "Enrollment Rejected": {"uz": "Ro'yxatdan O'tish Rad Etildi", "ru": "Регистрация отклонена"},
    "Course Lessons": {"uz": "Kurs Darslari", "ru": "Уроки курса"},
    "Completed": {"uz": "Tugatilgan", "ru": "Завершено"},
    "In Progress": {"uz": "Jarayonda", "ru": "В процессе"},
    "Locked": {"uz": "Yopiq", "ru": "Заблокировано"},
    "Complete previous lessons to unlock": {"uz": "Ochish uchun oldingi darslarni tugating", "ru": "Завершите предыдущие уроки, чтобы разблокировать"},
    "View Lesson": {"uz": "Darsni Ko'rish", "ru": "Посмотреть урок"},
    "Enrollment request submitted successfully!": {"uz": "Ro'yxatdan o'tish so'rovi muvaffaqiyatli yuborildi!", "ru": "Запрос на регистрацию успешно отправлен!"},
    "You are already enrolled or have a pending request.": {"uz": "Siz allaqachon ro'yxatdan o'tgansiz yoki kutilayotgan so'rovingiz bor.", "ru": "Вы уже зарегистрированы или у вас есть ожидающий запрос."},
    
    # Lesson page
    "materials": {"uz": "materiallar", "ru": "материалы"},
    "Back to Course": {"uz": "Kursga Qaytish", "ru": "Вернуться к курсу"},
    "Lesson Content": {"uz": "Dars Materiali", "ru": "Содержание урока"},
    "Learning Material": {"uz": "O'quv Materiali", "ru": "Учебный материал"},
    "Task": {"uz": "Topshiriq", "ru": "Задание"},
    "View Material": {"uz": "Materialni Ko'rish", "ru": "Посмотреть материал"},
    "Submit Task": {"uz": "Topshiriqni Yuborish", "ru": "Отправить задание"},
    "Submitted": {"uz": "Yuborilgan", "ru": "Отправлено"},
    "Passed": {"uz": "O'tdi", "ru": "Пройдено"},
    "Failed": {"uz": "O'tmadi", "ru": "Не пройдено"},
    "Pending Review": {"uz": "Ko'rib Chiqilmoqda", "ru": "Ожидает проверки"},
    "Score": {"uz": "Ball", "ru": "Оценка"},
    "Attempts": {"uz": "Urinishlar", "ru": "Попытки"},
    "No materials yet": {"uz": "Hali materiallar yo'q", "ru": "Материалов пока нет"},
    "This lesson doesn't have any materials yet. Check back later!": {"uz": "Bu darsda hali materiallar yo'q. Keyinroq qaytib tekshiring!", "ru": "В этом уроке пока нет материалов. Проверьте позже!"},
    "Mark as Completed": {"uz": "Bajarilgan deb Belgilash", "ru": "Отметить как завершенное"},
    "Material marked as completed!": {"uz": "Material bajarilgan deb belgilandi!", "ru": "Материал отмечен как завершенный!"},
    
    # Task submission page
    "Submit Your Answer": {"uz": "Javobingizni Yuboring", "ru": "Отправьте свой ответ"},
    "Attempt": {"uz": "Urinish", "ru": "Попытка"},
    "of": {"uz": "dan", "ru": "из"},
    "No attempts remaining": {"uz": "Urinishlar qolmadi", "ru": "Попыток не осталось"},
    "Task Instructions": {"uz": "Topshiriq Ko'rsatmalari", "ru": "Инструкции к заданию"},
    "Your Answer": {"uz": "Sizning Javobingiz", "ru": "Ваш ответ"},
    "Select your answer": {"uz": "Javobingizni tanlang", "ru": "Выберите ваш ответ"},
    "Select all that apply": {"uz": "Mos keladiganlarning barchasini tanlang", "ru": "Выберите все подходящие"},
    "Enter your answer here...": {"uz": "Javobingizni shu yerga kiriting...", "ru": "Введите ваш ответ здесь..."},
    "Submit Answer": {"uz": "Javobni Yuborish", "ru": "Отправить ответ"},
    "Cancel": {"uz": "Bekor Qilish", "ru": "Отмена"},
    "Answer submitted successfully!": {"uz": "Javob muvaffaqiyatli yuborildi!", "ru": "Ответ успешно отправлен!"},
    "You have reached the maximum number of attempts.": {"uz": "Siz maksimal urinishlar soniga yetdingiz.", "ru": "Вы достигли максимального количества попыток."},
    "This field is required.": {"uz": "Bu maydon to'ldirilishi shart.", "ru": "Это поле обязательно."},
    
    # Dashboard page
    "My Learning Progress": {"uz": "Mening O'quv Jarayonim", "ru": "Мой учебный прогресс"},
    "Track your progress across all courses": {"uz": "Barcha kurslardagi jarayoningizni kuzating", "ru": "Отслеживайте свой прогресс по всем курсам"},
    "Overall Progress": {"uz": "Umumiy Jarayon", "ru": "Общий прогресс"},
    "Passing Rate": {"uz": "O'tish Darajasi", "ru": "Процент прохождения"},
    "Course Progress Details": {"uz": "Kurs Jarayoni Tafsilotlari", "ru": "Детали прогресса курса"},
    "Lesson Progress": {"uz": "Dars Jarayoni", "ru": "Прогресс урока"},
    "Material Progress": {"uz": "Material Jarayoni", "ru": "Прогресс материала"},
    "Task Submissions": {"uz": "Topshiriqlar", "ru": "Представления заданий"},
    "Continue": {"uz": "Davom Ettirish", "ru": "Продолжить"},
    "Not enrolled in any courses yet": {"uz": "Hali hech qanday kursga yozilmagansiz", "ru": "Еще не записаны ни на один курс"},
    "Start your learning journey by enrolling in courses!": {"uz": "Kurslarga yozilib, o'quv sayohatingizni boshlang!", "ru": "Начните свое учебное путешествие, записавшись на курсы!"},
    
    # Submission history page
    "My Submission History": {"uz": "Mening Topshiriqlarim Tarixi", "ru": "История моих представлений"},
    "View all your task submissions and grades": {"uz": "Barcha topshiriqlaringiz va baholaringizni ko'ring", "ru": "Просмотрите все ваши представления и оценки"},
    "All Submissions": {"uz": "Barcha Topshiriqlar", "ru": "Все представления"},
    "Graded": {"uz": "Baholangan", "ru": "Оценено"},
    "Material": {"uz": "Material", "ru": "Материал"},
    "Submission Date": {"uz": "Yuborilgan Sana", "ru": "Дата представления"},
    "Status": {"uz": "Holat", "ru": "Статус"},
    "Feedback": {"uz": "Fikr", "ru": "Отзыв"},
    "No feedback provided": {"uz": "Fikr berilmagan", "ru": "Отзыв не предоставлен"},
    "No submissions yet": {"uz": "Hali topshiriqlar yo'q", "ru": "Представлений пока нет"},
    "Complete tasks to see your submission history here": {"uz": "Topshiriqlarni bajaring va bu yerda tarixingizni ko'ring", "ru": "Выполните задания, чтобы увидеть историю здесь"},
    
    # Profile page
    "My Profile": {"uz": "Mening Profilim", "ru": "Мой профиль"},
    "Teacher Profile": {"uz": "O'qituvchi Profili", "ru": "Профиль учителя"},
    "Edit Profile": {"uz": "Profilni Tahrirlash", "ru": "Редактировать профиль"},
    "Save Changes": {"uz": "O'zgarishlarni Saqlash", "ru": "Сохранить изменения"},
    "First Name": {"uz": "Ism", "ru": "Имя"},
    "Last Name": {"uz": "Familiya", "ru": "Фамилия"},
    "Enrolled Courses": {"uz": "Ro'yxatdan O'tgan Kurslar", "ru": "Записанные курсы"},
    "Passing Submissions": {"uz": "O'tgan Topshiriqlar", "ru": "Пройденные представления"},
    "Recent Submissions": {"uz": "So'nggi Topshiriqlar", "ru": "Недавние представления"},
    "No recent submissions": {"uz": "So'nggi topshiriqlar yo'q", "ru": "Нет недавних представлений"},
    "Quick Links": {"uz": "Tezkor Havolalar", "ru": "Быстрые ссылки"},
    "View Dashboard": {"uz": "Boshqaruv Panelini Ko'rish", "ru": "Посмотреть панель"},
    "Courses Managed": {"uz": "Boshqarilayotgan Kurslar", "ru": "Управляемые курсы"},
    "Profile updated successfully!": {"uz": "Profil muvaffaqiyatli yangilandi!", "ru": "Профиль успешно обновлен!"},
    
    # Error pages
    "Page Not Found": {"uz": "Sahifa Topilmadi", "ru": "Страница не найдена"},
    "Oops! The page you're looking for doesn't exist.": {"uz": "Uzr! Siz qidirayotgan sahifa mavjud emas.", "ru": "Упс! Страница, которую вы ищете, не существует."},
    "It might have been moved or deleted.": {"uz": "U ko'chirilgan yoki o'chirilgan bo'lishi mumkin.", "ru": "Она могла быть перемещена или удалена."},
    "Go to Home": {"uz": "Bosh Sahifaga O'tish", "ru": "Перейти на главную"},
    "Internal Server Error": {"uz": "Ichki Server Xatosi", "ru": "Внутренняя ошибка сервера"},
    "Something went wrong on our end.": {"uz": "Bizning tarafimizda nimadir noto'g'ri ketdi.", "ru": "Что-то пошло не так с нашей стороны."},
    "We're working to fix it. Please try again later.": {"uz": "Biz uni tuzatish ustida ishlayapmiz. Iltimos, keyinroq qayta urinib ko'ring.", "ru": "Мы работаем над исправлением. Пожалуйста, попробуйте позже."},
    "Try Again": {"uz": "Qayta Urinish", "ru": "Попробовать снова"},
    
    # Auth pages
    "Login to Basirat": {"uz": "Basirat'ga Kirish", "ru": "Войти в Basirat"},
    "Enter your phone number to continue": {"uz": "Davom etish uchun telefon raqamingizni kiriting", "ru": "Введите номер телефона, чтобы продолжить"},
    "Password": {"uz": "Parol", "ru": "Пароль"},
    "Login": {"uz": "Kirish", "ru": "Войти"},
    "Don't have an account?": {"uz": "Hisobingiz yo'qmi?", "ru": "Нет аккаунта?"},
    "Create Account": {"uz": "Hisob Yaratish", "ru": "Создать аккаунт"},
    "Create Your Account": {"uz": "Hisobingizni Yarating", "ru": "Создайте ваш аккаунт"},
    "Join Basirat and start learning": {"uz": "Basirat'ga qo'shiling va o'qishni boshlang", "ru": "Присоединяйтесь к Basirat и начните учиться"},
    "Already have an account?": {"uz": "Allaqachon hisobingiz bormi?", "ru": "Уже есть аккаунт?"},
    "Register": {"uz": "Ro'yxatdan O'tish", "ru": "Зарегистрироваться"},
    
    # Footer
    "© 2024 Basirat. All rights reserved.": {"uz": "© 2024 Basirat. Barcha huquqlar himoyalangan.", "ru": "© 2024 Basirat. Все права защищены."},
    
    # Model fields  
    "Title": {"uz": "Sarlavha", "ru": "Название"},
    "Slug": {"uz": "URL nomi", "ru": "URL имя"},
    "Summary": {"uz": "Qisqacha", "ru": "Краткое содержание"},
    "Description": {"uz": "Tavsif", "ru": "Описание"},
    "Is published": {"uz": "Nashr qilingan", "ru": "Опубликовано"},
    "Order": {"uz": "Tartib", "ru": "Порядок"},
    "Learning resource": {"uz": "O'quv materiali", "ru": "Учебный ресурс"},
    "Task/assignment": {"uz": "Topshiriq", "ru": "Задание"},
    "Single choice": {"uz": "Bitta tanlov", "ru": "Один выбор"},
    "Multiple choice": {"uz": "Ko'p tanlov", "ru": "Множественный выбор"},
    "Free response": {"uz": "Erkin javob", "ru": "Свободный ответ"},
    "Body text, transcript, or instructions written by administrators.": {"uz": "Matn, transkript yoki administratorlar yozgan ko'rsatmalar.", "ru": "Текст, транскрипт или инструкции, написанные администраторами."},
    "Upload videos, PDFs, images, or other assets that play inline.": {"uz": "Videolar, PDF-lar, rasmlar yoki boshqa fayllarni yuklang.", "ru": "Загрузите видео, PDF-файлы, изображения или другие ресурсы."},
    "Controls UI hints that discourage downloads/copying.": {"uz": "Yuklab olish/nusxalashni cheklaydigan UI ko'rsatmalarini boshqaradi.", "ru": "Управляет подсказками UI, которые препятствуют загрузке/копированию."},
    "Structured payload for task questions (choices, answers, hints).": {"uz": "Topshiriq savollari uchun tuzilgan ma'lumot (tanlovlar, javoblar, maslahatlar).", "ru": "Структурированные данные для вопросов заданий (выборы, ответы, подсказки)."},
}

def update_po_file(file_path, lang):
    """Update a .po file with translations"""
    import re
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_count = 0
    
    for english, trans in translations.items():
        if lang not in trans:
            continue
            
        translation = trans[lang]
        
        # Escape special characters for regex
        english_escaped = re.escape(english)
        
        # Pattern to match msgid followed by empty msgstr
        pattern = f'msgid "{english_escaped}"\\nmsgstr ""'
        replacement = f'msgid "{english}"\\nmsgstr "{translation}"'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            updated_count += 1
            print(f"  Updated: {english[:50]}...")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return updated_count

if __name__ == '__main__':
    import sys
    
    uz_file = 'locale/uz/LC_MESSAGES/django.po'
    ru_file = 'locale/ru/LC_MESSAGES/django.po'
    
    print("Updating Uzbek translations...")
    uz_count = update_po_file(uz_file, 'uz')
    print(f"✓ Updated {uz_count} Uzbek translations\n")
    
    print("Updating Russian translations...")
    ru_count = update_po_file(ru_file, 'ru')
    print(f"✓ Updated {ru_count} Russian translations\n")
    
    print(f"Total: {uz_count + ru_count} translations updated")
    print("\nNext steps:")
    print("1. Run: python manage.py compilemessages")
    print("2. Restart your Django server")
