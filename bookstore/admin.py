from django.contrib import admin
from .models import Book, Genre, Author

# Register your models here.
class BookInline(admin.StackedInline): #Demo StackedInline vs TabularInline
    model = Book
    fields = ('title',) 
    extra = 0
    
class GenreAdmin(admin.ModelAdmin):
    inlines = [BookInline,]
    
    model = Book


#http://stackoverflow.com/questions/6479999/django-admin-manytomany-inline-has-no-foreignkey-to-error    
#https://docs.djangoproject.com/en/dev/ref/contrib/admin/#working-with-many-to-many-models
class AuthorBookInline(admin.TabularInline): 
    model = Book.author.through
    extra = 0
    
class AuthorAdmin(admin.ModelAdmin):
    inlines = [AuthorBookInline,]
    model = Author

admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
