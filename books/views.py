from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm, ProfileForm


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.profile.regd_no = profile_form.cleaned_data.get('regd_no')
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
            user.profile.branch = profile_form.cleaned_data.get('branch')
            user.profile.year = profile_form.cleaned_data.get('year')
            user.profile.phone = profile_form.cleaned_data.get('phone')
            user.profile.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})
