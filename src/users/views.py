# coding: utf-8

from models import User
from forms import UserRegisterForm, UserLoginForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'sign_up_or_login.html', {
                'form': form,
            })
        else:
            data = form.cleaned_data
            del data['confirm_password']
            User.objects.create_user(**data)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
        return render(request, 'sign_up_or_login.html', {
            'form': form,
        })


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form['email'].value(), password=form['password'].value())
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('tasks:task_list'))
            else:
                return render(request, 'sign_up_or_login.html', {'form': form})
        else:
            return render(request, 'sign_up_or_login.html', {
                'form': form,
            })
    else:
        user = request.user
        if user.is_anonymous():
            form = UserLoginForm()
            return render(request, 'sign_up_or_login.html', {
                'form': form,
            })
        else:
            return HttpResponseRedirect(reverse('tasks:task_list'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
