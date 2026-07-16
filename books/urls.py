from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.book_upload, name='book_upload'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/download/', views.book_download, name='book_download'),
]
