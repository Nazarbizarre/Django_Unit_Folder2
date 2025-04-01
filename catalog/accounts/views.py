from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products:index")
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form":form})

