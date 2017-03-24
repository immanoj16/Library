from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


# class DateInput(forms.DateInput):
#     input_type = 'date'


# BRANCH_CHOICES = (
#     ('B.Tech', 'B.Tech'),
#     ('MCA', 'MCA'),
# )

# YEAR_CHOICES = (
#     ('1st', '1st'),
#     ('2nd', '2nd'),
#     ('3rd', '3rd'),
#     ('4th', '4th'),
#     ('5th', '5th'),
# )



class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = Profile
        fields = ( 'birth_date', 'bio', 'location')
