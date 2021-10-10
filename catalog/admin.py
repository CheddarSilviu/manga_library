from django.contrib import admin
from .models import Genre, Language, Book, BookInstance, Author


admin.site.register(Genre)
admin.site.register(Language)
	

class BookInlineMenu(admin.TabularInline):
	model = Book		


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInlineMenu]


admin.site.register(Author, AuthorAdmin)
class BookInstanceInlineMenu(admin.TabularInline):
	model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BookInstanceInlineMenu]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'book', 'borrower', 'status')

	list_filter = ('status', 'due_back')

	fieldsets = (
		(None, {'fields': ('book', 'imprint', 'id')}),
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')})
	)

