from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import Book, Student, IssueBook
from .forms import BookForm, StudentForm, IssueBookForm


# Home Page
def home(request):
    return render(request, 'library/home.html')


# Book List
@login_required
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
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'library/books/add_book.html', {'form': form})


# Edit Book
@login_required
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


@login_required
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('book_list')


# Student List
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'library/students/student_list.html', {'students': students})


# Add Student
@login_required
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
@login_required
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
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')

@login_required
def issue_book(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)

        if form.is_valid():

            already_issued = IssueBook.objects.filter(
                student=form.cleaned_data['student'],
                book=form.cleaned_data['book'],
                is_returned=False
            ).exists()

            if already_issued:
                messages.error(request, "This student has already issued this book.")
                return redirect('issue_book')

            issue = form.save(commit=False)
            issue.due_date = issue.issue_date + timedelta(days=7)

            # Check availability
            if issue.book.available > 0:
                issue.book.available -= 1
                issue.book.save()

                issue.save()

                messages.success(request, "Book issued successfully.")
                return redirect('issue_list')

            else:
                messages.error(request, "Book is not available.")
                return redirect('issue_book')

    else:
        form = IssueBookForm()

    return render(request, 'library/issue_book.html', {'form': form})
@login_required
def issue_list(request):
    issues = IssueBook.objects.all()
    return render(request, 'library/issue_list.html', {
        'issues': issues
    })

@login_required
def return_book(request, id):
    issue = get_object_or_404(IssueBook, id=id)

    if not issue.is_returned:
        issue.is_returned = True
        issue.return_date = timezone.now().date()

        # Fine Calculation
        if issue.return_date > issue.due_date:
            late_days = (issue.return_date - issue.due_date).days
            issue.fine = late_days * 10
        else:
            issue.fine = 0

        # Increase available books
        issue.book.available += 1
        issue.book.save()

        issue.save()

        messages.success(request, "Book returned successfully.")

    return redirect('issue_list')


@login_required
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