import uuid
from django.db import models
from django.urls import reverse



class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String representation of the Author."""
        return f'{self.last_name}, {self.first_name}'

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre")

    def __str__(self):
        return self.name

class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text="13 Character ISBN number")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    published_date = models.DateField(null=True, blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing a specific copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this book")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
class Meta:
    permissions = [("can_mark_returned", "Set book as returned")]

