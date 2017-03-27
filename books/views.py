from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import SignUpForm, ProfileForm, BookForm
from .models import Book, Issue


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
        context = {
            'book_form': BookForm(),
            'error_message': "Data is invalid",
        }
        return render(request, 'books/addbook.html', context)


@login_required
def search(request):
    username = request.user.username
    query = request.GET['q']
    if query:
        book_list = Book.objects.filter(Q(book_name__icontains=query)).distinct()
        user_list = User.objects.filter(Q(username__startswith=query)).distinct()
        context = {
            'book_list': book_list,
            'user_list': user_list,
            'username': username,
        }
        return render(request, 'books/search.html', context)
    else:
        book_list = Book.objects.order_by('book_name')[:50]
        context = {
            'error_message': "Please Give the book name or username",
            'book_list': book_list,
        }
        return render(request, 'books/home.html', context)


@login_required
def profile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return render(request, 'books/profile.html', )


@login_required
def issue(request, book_id):
    user = request.user
    choice = request.GET['choice']
    if choice == 'yes':
        book = get_object_or_404(Book, pk=book_id)

        book.no_of_books -= 1
        book.save()

        issue_book = Issue(issue_isbn_no=book.isbn_no, issue_book_name=book.book_name, user_id=user.id)
        issue_book.save()

        book_list = Book.objects.order_by('book_name')[:50]
        context = {
            'success_message': "The book has been issued...",
            'book_list': book_list,
        }
        return render(request, 'books/home.html', context)
    else:
        book_list = Book.objects.order_by('book_name')[:50]
        context = {
            'error_message': "Error occured!!!!",
            'book_list': book_list,
        }
        return render(request, 'books/home.html', context)
