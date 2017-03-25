from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from .forms import SignUpForm, ProfileForm, BookForm
from .models import Book


@login_required
def home(request):
    username = request.user.username
    book_list = Book.objects.order_by('book_name')[:50]
    return render(request, 'books/home.html', {'book_list': book_list, 'username': username})


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
    return render(request, 'books/signup.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def addbook(request):
    username = request.user.username
    if request.method == 'POST':
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book_form.save()

            book_list = Book.objects.order_by('book_name')[:50]
            context = {
                'success_message': "New book is added",
                'book_list': book_list,
                'username': username,
            }
            return render(request, 'books/home.html', context)

    else:
        book_form = BookForm()
        return render(request, 'books/addbook.html', {'book_form': book_form, 'error_message': "Data is invalid"})
