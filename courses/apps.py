from django.apps import AppConfig

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    
    def ready(self):
        # Этот метод запускается когда приложение готово
        from django.db.models.signals import post_migrate
        from .models import Course
        
        # Функция которая создает курсы после миграций
        def create_courses(sender, **kwargs):
            courses = [
                'Основы алгоритмизации и программирования', 
                'Основы веб-дизайна',  
                'Основы проектирования баз данных'  
            ]
            for name in courses:
                Course.objects.get_or_create(name=name)  # Создаем если нет
        
        # Подключаем нашу функцию к сигналу post_migrate
        post_migrate.connect(create_courses, sender=self)
