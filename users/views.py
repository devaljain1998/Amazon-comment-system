from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def regiser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are able to Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST ,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print(request.user.profile)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    content = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', content)

@login_required
def change_details(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            print(request.user.profile)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)


    content = {
        'u_form': u_form,
    }

    return render(request, 'users/change_details.html', content)

@login_required
def change_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST ,instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            print(request.user.profile)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)


    content = {
        'p_form': p_form
    }

    return render(request, 'users/change_profile.html', content)