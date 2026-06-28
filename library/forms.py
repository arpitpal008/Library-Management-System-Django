from django import forms
from .models import Book, Student, IssueBook

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        
class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssueBook
        fields = ['student', 'book']