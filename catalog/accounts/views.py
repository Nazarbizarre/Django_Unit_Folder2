from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileUpdateForm, RegisterFormNoCaptcha
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = request.POST.dict()
            # user = form.save()
            # login(request, user)
            # return redirect("products:index")
            new_email = form.cleaned_data.get("email")
            confirm_url = request.build_absolute_uri(reverse("accounts:confirm_email"))
            confirm_url += f"?email={new_email}"
            subject = "Confirm New Email"
            message = f"Hello, you want to confirm your email? " \
                            f"To confirm this operation click on link: {confirm_url}"
            send_mail(subject, message, from_email="noreply@gmail.com", recipient_list = [f"{new_email}"], fail_silently=False)
            messages.info(request, "Confirmation Email Sent!")
            return redirect("accounts:register")
    else:
        form = RegisterForm()
    request.session['last_visited'] = request.path
    return render(request, "register.html", context={"form":form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or 'products:index')
        else:
            return render(request, 'login.html', context={'error': 'Incorrect login or password'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('products:index')

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', context={"profile":profile})

@login_required
def edit_profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            # user.email = new_email
            # user.save()
            if new_email != user.email:
                confirm_url = request.build_absolute_uri(reverse("accounts:confirm_email"))
                confirm_url += f"?user={user.id}&email={new_email}"
                subject = "Confirm New Email"
                message = f"Hello, {user.username}, you want to change your email? " \
                            f"To confirm this operation click on link: {confirm_url}"
                send_mail(subject, message, from_email="noreply@gmail.com", recipient_list = [f"{new_email}"], fail_silently=False)
                messages.info(request, "Confirmation Email Sent!")
                
            avatar= form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(user=user)
    request.session['last_visited'] = request.path
    return render(request, "edit_profile.html", context={"form":form, "profile": profile})

def confirm_email(request):
    previous = request.session.get('last_visited')
    user_id = request.GET.get("user")
    email = request.GET.get("email")
    if not email:
        return HttpResponseBadRequest("Bad Request: No Email")
    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("This email is already taken")
    if previous == "/edit_profile/":
        if not user_id:
            return HttpResponseBadRequest("Bad Request: No User")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponseBadRequest("User Not Found")
        user.email = email
        user.save()
    else:
        form_data = request.session.get('form_data')
        if form_data:
            form_to_save = RegisterFormNoCaptcha(form_data)
            if form_to_save.is_valid():
                user = form_to_save.save()
                login(request, user)
    return render(request, "confirm_email.html", context={"email":email})

