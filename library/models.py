from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    available = models.PositiveIntegerField()
    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    fine = models.PositiveIntegerField(default=0)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.book.title}"