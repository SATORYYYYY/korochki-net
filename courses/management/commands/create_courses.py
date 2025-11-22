from django.core.management.base import BaseCommand
from courses.models import Course

# Создаем кастомную команду для Django - типа "магический скрипт" для наполнения базы данных
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Наши волшебные курсы, которые появятся в базе
        courses = [
            'Основы алгоритмизации и программирования', 
            'Основы веб-дизайна',                       
            'Основы проектирования баз данных'          
        ]
        
        # Проходим по каждому курсу как по красной дорожке
        for name in courses:
            # get_or_create - умный метод: ищет, если нет - создает. Как умный домофон
            Course.objects.get_or_create(name=name)
        
        # Кричим об успехе в консоль!
        self.stdout.write('Курсы созданы')