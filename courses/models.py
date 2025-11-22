from django.db import models
from django.contrib.auth.models import User

# Модель курса - основа основ, то чему мы учим
class Course(models.Model):
    name = models.CharField('Название курса', max_length=255)  # Название курса, не больше 255 символов
    
    def __str__(self):
        return self.name  # Чтобы в админке показывалось нормальное название
    
    class Meta:
        verbose_name = 'Курс'  # Красивое имя в единственном числе
        verbose_name_plural = 'Курсы'  # И во множественном тоже

# Дополнительная информация о пользователе - расширяем стандартного User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # Связь 1 к 1 с User
    phone = models.CharField('Телефон', max_length=20)  # Телефончик для связи
    address = models.CharField('Адрес', max_length=255)  # Адрес проживания

# Заявка на курс - типа "билет" на обучение
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # Кто подает заявку
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')  # На какой курс
    desired_start_date = models.DateField('Желаемая дата начала')  # Когда хочет начать
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=[
        ('cash', 'Наличными'),  # Бумажками
        ('transfer', 'Перевод по номеру телефона')  # По интернету
    ])
    status = models.CharField('Статус', max_length=20, choices=[
        ('new', 'Новая'),  # Только создана
        ('in_progress', 'Идет обучение'),  # Уже учится
        ('completed', 'Обучение завершено')  # Ура, закончил!
    ], default='new')  # По умолчанию новая
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # Автоматически ставится при создании
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def has_review(self):
        # Проверяем, есть ли отзыв к этой заявке - чтобы не писать дважды
        return hasattr(self, 'review')

# Модель отзыва - чтобы собирать мнения студентов
class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, verbose_name='Заявка')  # К какой заявке привязан отзыв
    rating = models.IntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])  # От 1 до 5 звезд
    comment = models.TextField('Комментарий')  # Текст отзыва
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # Когда оставили отзыв
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
# Create your models here.
