from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'uploaded_at', 'page_count', 'file_size_mb', 'is_approved']
    list_filter = ['is_approved', 'uploaded_at']
    search_fields = ['title', 'description', 'uploaded_by__username']
    list_editable = ['is_approved']
    ordering = ['-uploaded_at']
    readonly_fields = ['page_count', 'file_size_mb', 'uploaded_at']
