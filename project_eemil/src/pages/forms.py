from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import PasswordChangeForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required field. Enter a valid email address.')
    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2')


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords must match.')

        return new_password2

class TextModelForm(forms.ModelForm):
    class Meta:
        model = TextModel
        fields = ['text_data']

class MessageModelForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        exclude = ['message_sender']

class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = PwChangeModel
        fields = ['password', 'new_password']

class MessageGetForm(forms.ModelForm):
    class Meta:
        model = MessageGetModel
        fields = ['sender']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfoModel
        exclude = ['username']