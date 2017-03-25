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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': field,
                'class': 'form-control'
            })


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
    birth_date = forms.DateField(widget=DateInput())
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)

    class Meta:
        model = Profile
        fields = ('regd_no', 'birth_date', 'branch', 'year', 'phone')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': field,
                'class': 'form-control'
            })


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

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': field,
                'class': 'form-control'
            })
