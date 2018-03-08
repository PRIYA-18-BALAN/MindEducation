from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit("submit", "Submit"))

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def is_valid(self):
        if not super(LoginForm, self).is_valid():
            return False
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            if not user.check_password(self.cleaned_data['password']):
                self.add_error(None, 'Wrong Username or Password')
                return False
        except User.DoesNotExist, e:
            self.add_error(None, "Wrong Username")
            return False
        return True


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit("submit", "Submit"))

    def is_valid(self):
        if not super(RegistrationForm, self).is_valid():
            return False
        if self.cleaned_data['password'] != self.cleaned_data['password']:
            self.add_error('confirm_password', 'Passwords Donot Match')
            return False
        return True

    def save(self, commit=True):
        super(RegistrationForm, self).save()
        self.instance.set_password(self.instance.password)
        self.instance.save()
