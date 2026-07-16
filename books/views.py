from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
import os

from .models import Book
from .forms import BookUploadForm, CustomLoginForm, CustomSignupForm


# ─────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! 👋')
            next_url = request.GET.get('next', 'book_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Username ya password galat hai.')

    return render(request, 'books/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    form = CustomSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account ban gaya! Ab login karein.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    return render(request, 'books/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Aap logout ho gaye hain.')
    return redirect('login')


# ─────────────────────────────────────────
#  BOOK VIEWS (Login Required)
# ─────────────────────────────────────────

@login_required(login_url='/login/')
def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.filter(is_approved=True)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploaded_by__username__icontains=query)
        )

    return render(request, 'books/book_list.html', {
        'books': books,
        'query': query,
        'total_books': Book.objects.filter(is_approved=True).count(),
    })


@login_required(login_url='/login/')
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_approved=True)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required(login_url='/login/')
def book_upload(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            # File size calculate before save
            if book.pdf_file:
                book.file_size_mb = round(request.FILES['pdf_file'].size / (1024 * 1024), 2)
            book.save()
            messages.success(
                request,
                '📚 Book upload ho gayi! Admin approval ke baad library mein dikhegi.'
            )
            return redirect('book_list')
        else:
            messages.error(request, 'Kuch error hai — form dobara check karein.')
    else:
        form = BookUploadForm()

    return render(request, 'books/book_upload.html', {'form': form})


@login_required(login_url='/login/')
def book_download(request, pk):
    book = get_object_or_404(Book, pk=pk, is_approved=True)
    try:
        file_path = book.pdf_file.path
        if os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
            return response
        else:
            raise Http404("File nahi mila.")
    except Exception:
        raise Http404("File nahi mila.")
