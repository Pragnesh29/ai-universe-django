from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import Book


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'pdf_file', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter book title...',
                'id': 'id_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Enter a short description of the book...',
                'rows': 4,
                'id': 'id_description',
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': '.pdf',
                'id': 'id_pdf_file',
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*',
                'id': 'id_cover_image',
            }),
        }
        labels = {
            'title': 'Book Title',
            'description': 'Short Description',
            'pdf_file': 'Upload PDF File',
            'cover_image': 'Cover Image (optional)',
        }


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'id': 'id_email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Username',
            'id': 'id_username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password (min 8 chars, 1 uppercase, 1 special char)',
            'id': 'id_password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'id': 'id_password2',
        })
        # Remove default help text noise
        for field in self.fields.values():
            field.help_text = None

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not any(char.isupper() for char in password):
                raise ValidationError("Password must contain at least one uppercase letter.")
            # Special character check
            special_chars = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
            if not special_chars.search(password):
                raise ValidationError("Password must contain at least one special symbol.")
        return password


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Username',
            'id': 'id_login_username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password',
            'id': 'id_login_password',
        })

