from django.contrib import admin
from .models import Course, UserProfile, Application, Review

# Регистрируем наши модели в админке - делаем их видимыми для администратора
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']  # Показываем только имена курсов в списке

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Показываем пользователя и телефон - чтобы можно было позвонить и похвалить
    list_display = ['user', 'phone']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Вся важная информация о заявках в одном месте
    list_display = ['user', 'course', 'status', 'created_at']
    list_filter = ['status']  # Фильтр по статусу - чтобы не искать вручную
    actions = ['mark_as_completed']  # Наше кастомное действие - волшебная кнопка

    def mark_as_completed(self, request, queryset):
        # Превращаем все выбранные заявки в завершенные одним махом!
        queryset.update(status='completed')
    mark_as_completed.short_description = "Отметить как завершенные"  # Красивое название для кнопки

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Отзывы с рейтингом - чтобы видеть, кто как учился
    list_display = ['application', 'rating', 'created_at']
    list_filter = ['rating']  # Фильтруем по звездам - находим самых довольных
# Register your models here.
