from django.urls import path
from .views import edit, dashboard, register
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm
from django.db import models
from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserRegistrationModel
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetDoneView)

app_name = 'authapp'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='authapp/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authapp/password_change_form.html'), name='password_change'),
    path('password_change/dond/', PasswordChangeDoneView.as_view(template_name='authapp/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authapp/password_reset_form.html',
        email_template_name='authapp/password_reset_email.html',
        success_url=reverse_lazy('authapp:password_reset_done')), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='authapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='authapp/password_reset_confirm.html',
        success_url=reverse_lazy('authapp:login')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='authapp/password_reset_complete.html'), name='password_reset_complete'),

]
class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class AuthappConfig(AppConfig):
    name = 'authapp'

    def ready(self):
        from . import signals
default_app_config = 'authapp.apps.AuthappConfig'
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserRegistrationModel.objects.create(user=instance)
        profile.save()
LOGIN_REDIRECT_URL = 'authapp:dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))



#Frontend
{% load static %}
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
        integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">

    <!-- Font Awesome CDN -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/all.css"
        integrity="sha384-vp86vTRFVJgpjF9jiIGPEEqYqlDwgyBgEF109VFjmqGmIY/Y4HV4d3Gp2irVfcrp" crossorigin="anonymous">
    
        <!-- CSS -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">

    <title>App {% block title %}{% endblock title %}</title>
</head>

<body>
    {% include "navbar.html" %}
    <div class="container">
        {% block content %}

        {% endblock content %}
    </div>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous">
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous">
    </script>

    
</body>

</html>

#Navbar 
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="">Authentication <i class="fas fa-boxes"></i></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">

        {% if request.user.is_authenticated %}
        <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
                <a class="nav-link" href="{% url 'authapp:dashboard' %}">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link " href="#">Dashboard</a>
            </li>
        </ul>
        {% endif %}
        <span>
            {% if request.user.is_authenticated %}
            <a href="{% url 'authapp:logout' %}" class="btn btn-danger">Logout</a>
            Hello
            @ <i>{{user.username}}</i>
            {% else %}
            <div class="login__left">
                <a href="{% url 'authapp:login' %}" class="btn btn-secondary">Log-in</a>
                <a href="{% url 'authapp:register' %}" class="btn btn-info ">Register</a>
            </div>

            {% endif %}

        </span>
    </div>
</nav>

#login.html
{% extends "base.html" %}
{% load bootstrap4 %}
{% block title %}Login{% endblock title %}

{% block content %}
<div class="">
    <div style="text-align: center;">
        <h1>Log-in</h1>
        {% if form.errors %}
        <p>
            Your username and password didn't match.Please
            Please try again.
        </p>
        {% else %}
        <p>Please, use the following form to log-in</p>
        {% endif %}
    </div>

    <form action="" method="post" class="form ">
        <p><a href="{% url 'authapp:password_reset' %}">Forgotten your password?</a></p>
        {% csrf_token %}
        {% bootstrap_form form %}
        {% buttons %}
        <input type="hidden" name="next" value="{{ next }}" />
        <button type="submit" class="btn btn-primary">Submit</button>
        {% endbuttons %}
    </form>
</div>
{% endblock content %}
{% extends "base.html" %}
{% block title %}Dashboard{% endblock title %}
{% block content %}
<h1>{{welcome}}</h1>
<br>
<a href="{% url 'authapp:edit' %}" class="btn btn-primary">Edit Your Profile</a> or
<a href="{% url 'authapp:password_change' %}" class="btn btn-warning">Change your password</a>
<hr>
{% endblock content %}
{% extends "base.html" %}
{% load bootstrap4 %}
{% block title %}Edit{% endblock title %}
{% block content %}
<h2>Edit your account</h2>
<p>You can edit your account using the follow form</p>
<form action="" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
{% endblock content %}
#logged out
{% extends "base.html" %}
{% block title %}Logged out{% endblock %}
{% block content %}
<h1>Logged out</h1>
<p>
    You have been successfully logged out.
    <hr>
    You can <a href="{% url 'authapp:login' %}">log-in again</a>.
</p>
{% endblock %}

#password_change
{% extends "base.html" %}
{% load bootstrap4 %}
{% block content %}
<h2>Change Your Password</h2>
<p>Use the form below to change your Password</p>
<form action="" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
{% endblock content %}


# password reset
{% extends "base.html" %}
{% block title %}Password reset{% endblock %}
{% block content %}
<h2>Password set</h2>
<p>Your password has been reset. You can
    <a href="{% url 'authapp:login' %}">log in now</a></p>
{% endblock %}

#password reset confirm
{% extends "base.html" %}
{% load bootstrap4 %}
{% block title %}Reset your password{% endblock %}
{% block content %}
<h1>Reset your password</h1>
{% if validlink %}
<p>Please enter your new password twice:</p>
<form action="" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
    <button type="submit" class="btn btn-primary" value="Change my password">Submit</button>
    {% endbuttons %}
</form>
{% else %}
<p>The password reset link was invalid, possibly because it has
    already been used. Please request a new password reset.</p>
{% endif %}
{% endblock %}


{% extends "base.html" %}
{% load bootstrap4 %}
{% block title %}Reset your password{% endblock %}
{% block content %}
<h1>Reset your password</h1>
{% if validlink %}
<p>Please enter your new password twice:</p>
<form action="" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
    <button type="submit" class="btn btn-primary" value="Change my password">Submit</button>
    {% endbuttons %}
</form>
{% else %}
<p>The password reset link was invalid, possibly because it has
    already been used. Please request a new password reset.</p>
{% endif %}
{% endblock %}

{% extends "base.html" %}
{% block title %}Reset your password{% endblock %}
{% block content %}
<h1>Reset your password</h1>
<p>We've emailed you instructions for setting your password.</p>
<p>If you don't receive an email, please make sure you've entered
    the address you registered with.</p>
{% endblock %}

Someone asked for password reset for email {{email}}.Follow the Link below
{{ protocol }}://{{ domain }}{% url "authapp:password_reset_confirm"
uidb64=uid token=token %}

Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password reset on 127.0.0.1:8000
From: webmaster@localhost
To: test@yahoo.com
Date: Thu, 22 Oct 2020 10:43:58 -0000
Message-ID: <160336343867.13084.17624992201475370147@DESKTOP-8LLQCDQ>

Someone asked for password reset for email test@yahoo.com.Follow the Link below
http://127.0.0.1:8000{% url "authapp:password_reset_confirm" uidb64=uid token=token %}


{% extends 'base.html' %}
{% load bootstrap4 %}
{% block title %}Reset your password

{% endblock title %}
{% block content %}
<div class="container">
    <h2>Forgotten your Password</h2>
    <p>Enter your email address to obtain a new password</p>
    <form action="" method="post" class="form ">
        {% csrf_token %}
        {% bootstrap_form form %}
        {% buttons %}
        <button type="submit" class="btn btn-primary" value="send e-mail">Submit</button>
        {% endbuttons %}
    </form>
</div>
{% endblock content %}

{% extends "base.html" %}
{% load bootstrap4 %}
{% block title %}Registration

{% endblock title %}
{% block content %}

{% if form.errors %}
    
{% endif %}
    
<form action="" method="post" class="form container">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
    <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
{% endblock content %}

{% extends "base.html" %}
{% block content %}
<h1>Welcome {{ new_user.first_name }}!</h1>
<p>Your account has been successfully created. Now you can <a href="{% url 'authapp:login' %}">log in</a>.</p>
{% endblock content %}