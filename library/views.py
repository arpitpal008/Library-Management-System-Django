from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Student, IssueBook
from .forms import BookForm, StudentForm, IssueBookForm

# Home Page
def home(request):
    return render(request, 'library/home.html')


# Book List
def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'library/books/book_list.html', {
        'books': books
    })

# Add Book
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'library/books/add_book.html', {'form': form})


# Edit Book
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'library/books/add_book.html', {'form': form})



def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('book_list')


# Student List
def student_list(request):
    students = Student.objects.all()
    return render(request, 'library/students/student_list.html', {'students': students})


# Add Student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'library/students/add_student.html', {'form': form})


# Edit Student
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'library/students/add_student.html', {'form': form})


# Delete Student
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')


def issue_book(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)

        if form.is_valid():
            issue = form.save(commit=False)

            # Check availability
            if issue.book.available > 0:
                issue.book.available -= 1
                issue.book.save()

                issue.save()

                return redirect('issue_list')

    else:
        form = IssueBookForm()

    return render(request, 'library/issue_book.html', {'form': form})

def issue_list(request):
    issues = IssueBook.objects.all()
    return render(request, 'library/issue_list.html', {
        'issues': issues
    })
    
    
    
from django.utils import timezone

def return_book(request, id):
    issue = get_object_or_404(IssueBook, id=id)

    if not issue.is_returned:
        issue.is_returned = True
        issue.return_date = timezone.now()

        issue.book.available += 1
        issue.book.save()

        issue.save()

    return redirect('issue_list')


from django.db.models import Sum

def dashboard(request):
    total_books = Book.objects.count()
    total_students = Student.objects.count()
    issued_books = IssueBook.objects.filter(is_returned=False).count()
    available_books = Book.objects.aggregate(total=Sum('available'))['total'] or 0

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'issued_books': issued_books,
        'available_books': available_books,
    }

    return render(request, 'library/dashboard.html', context)