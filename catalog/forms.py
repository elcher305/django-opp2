from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser


class ChangeUserInfoForm(forms.ModelForm):
   email = forms.EmailField(required=True, label='Адрес электронной почты')

   class Meta:
       model = AdvUser
       fields = ('username', 'email', 'fio')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,help_text='Повторите тот же самый пароль еще раз'
    )
    fio = forms.CharField(label='ФИО', max_length=100)
    username = forms.CharField(label='Логин', max_length=30)
    consent = forms.BooleanField(label='Согласие на обработку персональных данных')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError(
                'Введенные пароли не совпадают.'
            ))


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'fio', 'email', 'password1', 'password2', 'consent')