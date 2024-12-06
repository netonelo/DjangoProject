from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Определите класс администрирования для Author
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# Зарегистрируйте Author с кастомным классом администрирования
admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# Определите класс администрирования для BookInstance
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')


# Зарегистрируйте Genre без кастомного класса администрирования
admin.site.register(Genre)