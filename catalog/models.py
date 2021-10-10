from django.db import models 
import uuid 	
from django.urls import reverse
import datetime
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):

	name = models.CharField(max_length = 200, help_text='Genre, e.g. Manga, Shunen, Art Manga"')	

	def __str__(self):
		return self.name


class Language(models.Model):

	name = models.CharField(max_length = 200, help_text = 'Language')

	def __str__(self):
		return self.name


class Book(models.Model):

	title = models.CharField(max_length = 200)
	author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)
	summary = models.TextField(max_length = 1300, help_text = 'Enter book description')
	isbn = models.CharField('ISBN', max_length = 13, unique = True, help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	genre = models.ManyToManyField(Genre, help_text = 'Genre: Shonen, Shojo..')
	language = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True)


	class Meta:
		ordering = ['title', 'author']

	def display_genre(self):
		return ', '.join(genre.name for genre in self.genre.all()[:3])

	display_genre.short_description = 'Genre'

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def __str__(self):
		return self.title



class BookInstance(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = 'Unique ID for this particular book across the whole library')
	book = models.ForeignKey('Book', on_delete = models.RESTRICT, null = True)
	imprint = models.CharField(max_length = 250, help_text = 'Publishing details')
	due_back = models.DateField(null = True, blank = True)
	borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False


	LOAN_STATUS = (
				('m', 'Maintenance'),
				('o', 'On loan'),
				('a', 'Available'),
				('r', 'Reserverd'),
		)


	status = models.CharField(max_length = 1, 
							  choices = LOAN_STATUS, 
							  blank = True, 
							  default = 'm',
							  help_text = 'Book availability')
	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_returned", "Set book as returned"),)

	def __str__(self):
		return f'{self.id}  {self.book.title}'

		

class Author(models.Model):

	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	date_of_birth = models.DateField(null = True,blank = True)
	date_of_death = models.DateField('died', null = True,blank = True)

	class Meta:
		ordering = ['last_name', 'first_name']


	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'
