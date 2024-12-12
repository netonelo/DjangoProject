from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Укажите жанр книги (например, научная фантастика, французская поэзия и т. д.)", verbose_name=("Жанр"))

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name=("Название"))
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name=("Автор"))
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги", verbose_name=("Описание"))
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр(ы) книги", verbose_name=("Жанр"))

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID этой конкретной книги во всей библиотеке.", verbose_name=("ID"))
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name=("Книга"))
    imprint = models.CharField(max_length=200, verbose_name=("Штамп(год выпуска)"))
    due_back = models.DateField(null=True, blank=True, verbose_name=("Дата возвращения книги"))
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=("Заёмщик"))

    LOAN_STATUS = (
        ('m', 'Книга на тех. обслуживании'),
        ('o', 'Взята'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Статус книги', verbose_name=("Статус"))

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=("Имя"))
    last_name = models.CharField(max_length=100, verbose_name=("Фамилия"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=("Дата рождения"))
    date_of_death = models.DateField('Умер', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)