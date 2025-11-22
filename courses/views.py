from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ApplicationForm, ReviewForm
from .models import Application, UserProfile, Review

# Главная страница - входная дверь в наш сайт
def home(request):
    return render(request, 'home.html')  # Просто показываем шаблон home.html

# Регистрация новых пользователей - типа "запись в клуб"
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Получаем данные из формы
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            # Дополняем стандартного User нашими полями
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Создаем профиль с телефоном и адресом
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            login(request, user)  # Автоматически логиним пользователя
            messages.success(request, 'Регистрация прошла успешно!')  # Показываем "ура!"
            return redirect('application_list')  # Отправляем к заявкам
    else:
        form = RegisterForm()  # Пустая форма для GET запроса
    return render(request, 'register.html', {'form': form})

# Кастомный вход - проверяем логин/пароль
def custom_login(request):
    if request.method == 'POST':
        # Проверяем, есть ли такой пользователь
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)  # Если есть - пускаем
            return redirect('application_list')
        messages.error(request, 'Неверный логин или пароль')  # Если нет - ругаемся
    return render(request, 'login.html')

# Выход - просто разлогиниваем и отправляем на главную
def custom_logout(request):
    logout(request)
    return redirect('home')

# Список заявок пользователя - только для залогиненных
@login_required
def application_list(request):
    # Показываем только заявки текущего пользователя
    applications = Application.objects.filter(user=request.user)
    return render(request, 'application_list.html', {'applications': applications})

# Создание новой заявки - "хочу на курс!"
@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)  # Не сохраняем сразу
            application.user = request.user  # Привязываем к текущему пользователю
            application.save()  # Теперь сохраняем
            messages.success(request, 'Заявка успешно создана!')
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})

# Создание отзыва - только для завершенных курсов
@login_required
def create_review(request, application_id):
    # Находим заявку или показываем 404 ошибку
    application = get_object_or_404(Application, id=application_id, user=request.user)
    
    # Проверяем, что курс завершен - нельзя хвалить то, что не закончил
    if application.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('application_list')
    
    # Проверяем, что отзыв еще не оставлен - один отзыв на курс!
    if hasattr(application, 'review'):
        messages.error(request, 'Вы уже оставили отзыв для этого курса')
        return redirect('application_list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application  # Привязываем отзыв к заявке
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')  # Благодарим
            return redirect('application_list')
    else:
        form = ReviewForm()
    
    return render(request, 'create_review.html', {'form': form, 'application': application})
# Create your views here.
