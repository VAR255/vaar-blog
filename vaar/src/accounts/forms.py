from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from . models import Profile


class PwdchangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'
    }))
    



class PwdResetComfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass1'}
        )
    )

    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass2'}
        )
    )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email'] 
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'Unifortunatley we can not find that email address'
            )
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Password', 'id': 'login-pwd'
    }))


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Usenname', min_length=4, max_length=50, help_text='Required'
    )

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'
    })

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields = ('username', 'email', 'password', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password do not much')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken'
            )
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'}
        )

        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'}
        )

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )

        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'}
        )



class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'login-first_name'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Last name', 'id': 'login-last_name'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'login-email'
    }))

    class Meta:
        model=User
        fields = ('first_name','last_name', 'email')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

        widgets = {
            'bio':forms.Textarea(attrs={
                'class': 'form-control', 'rows': '5'
            })
        }
