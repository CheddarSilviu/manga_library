from django.shortcuts import render
# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language

def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
	num_authors = Author.objects.all().count()

	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	# num_genres = Genre.objects.all().count()
	# num_languages = Language.objects.all().count()
	particular_books = Book.objects.filter(title__icontains = 'berserk')[:2].count()

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		# 'num_genres':num_genres,
		# 'num_languages':num_languages,
		'particular_books':particular_books,
		'num_visits': num_visits,
	}

	return render(request, 'index.html', context = context)

from django.views import generic



class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 10


class AuthorDetailView(generic.DetailView):
	model = Author


from django.contrib.auth.mixins import LoginRequiredMixin



class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksByLibrarianListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact= 'o').order_by('due_back')



#part of form construction view

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required
# from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm


@permission_required('catalog.can_mark_returned', raise_exception = True)
def renew_book_librarian(request, pk):
		book_instance = get_object_or_404(BookInstance, pk = pk)

		#if POST, request then process data
		if request.method == 'POST':

			# form = RenewBookForm(request.POST)
			form = RenewBookModelForm(request.POST)

			#check if form is valid
			if form.is_valid():
				book_instance.due_back = form.cleaned_data['renewal_date']
				book_instance.save()

				return HttpResponseRedirect(reverse('all-librarian'))

		else:
			proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
			# form = RenewBookForm(initial = {'renewal_date': proposed_renewal_date})
			form = RenewBookModelForm(initial = {'due_back': proposed_renewal_date})

		context = {
				'form':form,
				'book_instance': book_instance,
		}

		return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author
from catalog.models import Book


class AuthorCreate(PermissionRequiredMixin, CreateView):
		model = Author
		fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
		initial = {'date_of_death': '11/06/2002'}
		permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
		model = Author
		fields = '__all__'
		permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
		model = Author
		success_url = reverse_lazy('authors')
		permission_required = 'catalog.can_mark_returned'



class BookCreate(PermissionRequiredMixin, CreateView):
		model = Book
		fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
		permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
		model = Book
		fields = '__all__'
		permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
		model = Book
		success_url = reverse_lazy('books')
		permission_required = 'catalog.can_mark_returned'






