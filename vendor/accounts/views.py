from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, AddressForm
from .models import Address
from django.contrib import messages

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # change if needed
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")



def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'addresses': addresses})

from .forms import UserUpdateForm
from django.contrib import messages

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form})
