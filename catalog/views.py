import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView  # Import DetailView
from catalog.forms import RenewBookForm
from catalog.models import BookInstance, Book  # Ensure Book is imported
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from catalog.models import Book, BookInstance, Author
from django.shortcuts import render


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by a librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

def index(request):
    return render(request, 'catalog/index.html')

class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'  # Ensure this template exists
    context_object_name = 'book_list'  

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'  # Ensure this template exists
    context_object_name = 'book'  # Optional: Customize the context variable



def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect after login
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


def index(request):
    """View function for home page of site."""
    
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context)  # Corrected path