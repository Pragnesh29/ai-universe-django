from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Book


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'pdf_file', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Book ka naam likhein...',
                'id': 'id_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Book ki short description likhein...',
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
            'pdf_file': 'PDF File Upload karo',
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
            'placeholder': 'Password',
            'id': 'id_password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password confirm karein',
            'id': 'id_password2',
        })
        # Remove default help text noise
        for field in self.fields.values():
            field.help_text = None


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
