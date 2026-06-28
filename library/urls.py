from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:id>/', views.delete_book, name='delete_book'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('issue/', views.issue_book, name='issue_book'),
    path('issue/list/', views.issue_list, name='issue_list'),
    path('return/<int:id>/', views.return_book, name='return_book'),
    path('dashboard/', views.dashboard, name='dashboard'),
]