from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.warning(request, "Вы успешно вошли в свой аккаунт")
                return redirect("main:home")

            else:

                redirect('login')

    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "pages/login.html", context)

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')




    else:
        form = RegistrationForm()
    context = {
        "form": form
    }
    return render(request, "pages/registration.html", context)

def logout_view(request):
    logout(request)
    return redirect('main:home')

