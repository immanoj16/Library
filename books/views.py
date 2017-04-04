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
                'message': "New book is added",
                'book_list': book_list,
                'username': username,
            }
            return render(request, 'books/home.html', context)

    else:
        context = {
            'book_form': BookForm(),
            'message': "Data is invalid",
        }
        return render(request, 'books/addbook.html', context)


@login_required
def remove_book(request):
    username = request.user.username
    if username == 'admin':
        isbn_no = request.GET.get('isbn_no','')
        try:
            book = Book.objects.get(isbn_no=isbn_no)
            book.delete()
            book_list = Book.objects.order_by('book_name')[:50]
            context = {
                'message': "The book is removed",
                'book_list': book_list,
            }
            return render(request, 'books/home.html', context)
        except:
            return render(request, 'books/remove_book.html', {'message': "Give correct Id or Name"})
    else:
        return render(request, 'books/remove_book.html', {'message': "Give correct Id or Name"})


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
            'message': "Please Give the book name or username",
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

        issued_book = user.issue_set.filter(issue_isbn_no__iexact=book.isbn_no)

        if not issued_book:

            book.no_of_books -= 1
            book.save()

            issue_book = user.issue_set.create(issue_isbn_no=book.isbn_no, issue_book_name=book.book_name)
            print issue_book
            print issue_book.user.id

            book_list = Book.objects.order_by('book_name')[:50]
            context = {
                'message': "The book has been issued...",
                'book_list': book_list,
            }
            return render(request, 'books/home.html', context)
        else:
            book_list = Book.objects.order_by('book_name')[:50]
            context = {
                'message': "You have already issued this book...",
                'book_list': book_list,
            }
            return render(request, 'books/home.html', context)

    else:
        book_list = Book.objects.order_by('book_name')[:50]
        context = {
            'message': "Error occured!!!!",
            'book_list': book_list,
        }
        return render(request, 'books/home.html', context)


@login_required
def issue_list(request):
    user = request.user
    # user = User.objects.get(username=request.user.username)
    list = user.issue_set.order_by('issue_book_name')
    return render(request, 'books/issue_list.html', {'list': list,})


@login_required
def add_user(request):
    if request.user.username == 'admin':
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
                book_list = Book.objects.order_by('book_name')[:50]
                context = {
                    'message': "new user is added named " + user.username,
                    'book_list': book_list,
                }
                return render(request, 'books/home.html', context)
        else:
            user_form = SignUpForm()
            profile_form = ProfileForm()
        return render(request, 'books/add_user.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def remove_user(request):
    username = request.user.username
    if username == 'admin':
        user_name = request.GET.get('user_name', '')
        try:
            user = User.objects.get(username=user_name)
            user.delete()
            book_list = Book.objects.order_by('book_name')[:50]
            context = {
                'message': "The user is removed",
                'book_list': book_list,
            }
            return render(request, 'books/home.html', context)
        except:
            return render(request, 'books/remove_user.html', {'message': "Give correct Id or Name"})
    else:
        return render(request, 'books/remove_user.html', {'message': "Give correct Id or Name"})


@login_required
def users(request):
    username = request.user.username
    if username == 'admin':
        user_list = User.objects.order_by('username')[:50]
        return render(request, 'books/users.html', {'user_list': user_list, 'username': username})
    else:
        book_list = Book.objects.order_by('book_name')[:50]
        context = {
            'book_list': book_list,
            'username': username,
            'message': "It shows only to admin..."
        }
        return render(request, 'books/home.html', context)

