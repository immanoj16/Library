from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Book


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class DateInput(forms.DateInput):
    input_type = 'date'


BRANCH_CHOICES = (
    ('B.Tech', 'B.Tech'),
    ('MCA', 'MCA'),
)

YEAR_CHOICES = (
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),
)


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)

    class Meta:
        model = Profile
        fields = ('regd_no', 'birth_date', 'branch', 'year', 'phone')

        widgets = {
            'birth_date': DateInput(),
        }


BOOK_CHOICES = (
    ('Programming', 'Programming'),
    ('Computer', 'Computer'),
    ('Math', 'Math'),
    ('Economics', 'Economics'),
    ('Accounting', 'Accounting'),
    ('Others', 'Others')
)


class BookForm(forms.ModelForm):
    book_type = forms.ChoiceField(choices=BOOK_CHOICES)

    class Meta:
        model = Book
        fields = ('isbn_no', 'book_name', 'author_name', 'book_type', 'edition', 'no_of_books')
