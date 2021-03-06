from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Genre(models.Model):
    name= models.CharField(max_length=200, help_text="Genre")
    
    def __str__(self):
        return self.name


class Language(models.Model):
    name= models.CharField(max_length=50, help_text="Language")

    def __str__(self):
        return self.name


class Book(models.Model):
    title= models.CharField(max_length=170, help_text="Title")
    author= models.ForeignKey('Author', on_delete=models.SET_NULL, null= True)
    summary= models.TextField(max_length= 100, help_text="Brief description of the book")
    isbn= models.CharField('ISBN', max_length= 13, help_text= "isbn")
    genre= models.ManyToManyField(Genre, help_text= "Select genre")
    language= models.ForeignKey('Language', on_delete= models.SET_NULL, null= True)

    def display_genre(self):
        return ','.join([genre.name for genre in self.genre.all()[:3]])
    
    display_genre.short_description= 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args= [str(self.id)])

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    id= models.UUIDField(primary_key= True, default=uuid.uuid4, help_text= "Unique ID for this particular book")
    book= models.ForeignKey('Book', on_delete= models.SET_NULL, null= True)
    imprint= models.CharField(max_length= 200)
    due_back= models.DateField(null= True, blank= True)
    borrower= models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)

    @property
    def is_overdue(self):
        if self.due_back and date.today()> self.due_back:
            return True
        return False

    Loan_statuses= (
        ('m', 'Maintenance'),
        ('a', 'Available'),
        ('r', 'reserved'),
        ('o', 'On loan')
    )

    status= models.CharField(max_length= 1, choices= Loan_statuses, blank= True, default= 'm', help_text= 'Book Availability')

    class Meta:
        ordering= ['due_back']
        permissions= (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    first_name= models.CharField(max_length= 50)
    last_name= models.CharField(max_length= 50)
    date_of_birth= models.DateField(null= True, blank= True)
    date_of_death= models.DateField('died', null= True, blank= True)

    class Meta:
        ordering= ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author_detail', args= [str(self.id)])

    def __str__(self):
        return '{0}, {1}'. format(self.last_name, self.first_name)
    