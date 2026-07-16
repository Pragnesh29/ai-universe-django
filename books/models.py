from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='books/pdfs/')
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    page_count = models.PositiveIntegerField(default=0)
    file_size_mb = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)  # Admin approval required

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-detect file size in MB
        if self.pdf_file and hasattr(self.pdf_file, 'size'):
            self.file_size_mb = round(self.pdf_file.size / (1024 * 1024), 2)
        super().save(*args, **kwargs)
        # Auto-detect page count after save (file is now on disk)
        if self.pdf_file and self.page_count == 0:
            try:
                from pypdf import PdfReader
                reader = PdfReader(self.pdf_file.path)
                self.page_count = len(reader.pages)
                Book.objects.filter(pk=self.pk).update(page_count=self.page_count)
            except Exception:
                pass
