from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

def user_aut(request):
    # Добавляем переменную caption1 в контекст
    context = {'caption1': 'Цветочного магазина'}  # Значение переменной
    return render(request, 'user/user_aut.html', context)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



    def user_aut(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cabinet')
            else:
                return render(request, 'user/user_aut.html', {'error': 'Неверные данные'})
        return render(request, 'user/user_aut.html')

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('cabinet')
        else:
            form = UserCreationForm()
        return render(request, 'user/register.html', {'form': form})

    def password_reset(request):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(
                    request=request,
                    email_template_name='user/password_reset_email.html',
                    subject_template_name='user/password_reset_subject.txt',
                )
                return redirect('password_reset_done')
        else:
            form = PasswordResetForm()
        return render(request, 'user/password_reset.html', {'form': form})

    def password_reset_confirm(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

"""       if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = PasswordResetConfirmForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('password_reset_complete')
            else:
                form = PasswordResetConfirmForm(user=user)
            return render(request, 'user/password_reset_confirm.html', {'form': form})
        else:
            return render(request, 'user/password_reset_confirm_invalid.html')
"""



def register(request):
    # Код для регистрации
    pass

def password_reset(request):
    # Код для восстановления пароля
    pass