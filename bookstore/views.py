from django.shortcuts import render
from django.http import HttpResponse
#from .models import Book
from django.core.urlresolvers import reverse
import re
from django.db.models import Q
from django.views.generic import ListView
from .models import Book
from django.views.generic.edit import CreateView
from bookstore.forms import BookForm
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from .models import Book, Genre, Author
from .forms import BookForm, GenreForm, AuthorForm
from django.views.generic import DetailView, ListView, TemplateView

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile

class MyView(TemplateView):
    #setup the various forms in this view
    genre_form_class = GenreForm
    author_form_class = AuthorForm
    book_form_class = BookForm
    template_name = "bookstore/book_hybrid.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)


    #called when loading the page for a new entry
    def get(self, request, *args, **kwargs):
        #setup all the forms by intialising the various form names with the corresponding form class
        kwargs.setdefault("addgenre_form", self.genre_form_class())
        kwargs.setdefault("addauthor_form", self.author_form_class())
        kwargs.setdefault("addbook_form", self.book_form_class())
         #Added curruser so that profile picture of curruser can be rendered.
        #kwargs.setdefault('curruser', UserProfile.objects.get(user=self.request.user))

        return super(MyView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
        }
        
        #if btn_createfolder hidden field is a value in POST form
        if "btn_creategenre" in request.POST['form']: 
            form = self.folder_form_class(**form_args)
            #check if form is not value, reload the form with the POST values
            if not form.is_valid():
                #Construct the failed status (0) and the errors as message to be displayed in the template
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
            else:
                #form is valid, save the form, and return all folders as data to update the folder select list
                form.save()
                data = Genre.objects.all()
                response_dict = {'status': 1}
                response_dict['message'] = list(data.values('id','title'))
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
        #if btn_createtag hidden field is a value in POST form
        elif "btn_createauthor" in request.POST['form']: 
            form = self.tag_form_class(**form_args)
            if not form.is_valid():
                #Construct the failed status (0) and the errors as message to be displayed in the template
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
                #return self.get(request, createtag_form=form)
            else:
                #form is valid, save the form, and return all folders as data to update the tag multi-select list
                form.save() #save the new object
                data = Author.objects.all() # retrieve all records
                response_dict = {'status': 1}
                response_dict['message'] = list(data.values('id','title'))
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
        #if btn_createnote hidden field is a value in POST form
        elif "btn_addbook" in request.POST['form']:
            form = self.note_form_class(**form_args)
            if not form.is_valid():
                #Construct the failed status (0) and the errors as message to be displayed in the template
                response_dict = {}
                response_dict['status'] = 0
                response_dict['message'] = form.errors.as_ul()
                return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
                #return self.get(request, createnote_form=form, errors=response_dict) 
            else:
                #form is valid, save the form, and return all folders as data to update the tag multi-select list
                try:
                    #Find out which user is logged in and get the correct UserProfile record.
                    curruser = UserProfile.objects.get(user=self.request.user)
                    obj = form.save(commit=False)
                    obj.user = curruser #Save the note note under that user
                    obj.save() #save the new object
                    
                except Exception, e:
                    print("errors" + str(e))
                response = {'status': 1, 'message':'ok'}
                return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
            
        return super(MyView, self).get(request)


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('listall')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookDelete, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookDelete, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class BookCreate(CreateView):
    model = Book
    form_class = BookForm
    
class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookUpdate, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(NoteUpdate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class BookDetail(DetailView):
    model = Book
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookDetail, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context



# Create your views here.
def bookstore_list(request, genre):
    if genre == "":
        all_books = Book.objects.all().order_by("genre__title")
        total = all_books.count()
    else:
        all_books = Book.objects.filter(genre__title__iexact=genre)
        total = all_books.count()
    return render(request, 'bookstore/index.html', {'bookstore': all_books, 'total': total})

def bookstore_author(request, author):
    pieces = author.split('/') #extract different tags separated by /
    # allnotes = Note.objects.none() #required when doing normal filter pipe query ... see below
    #for p in pieces:
        #This is to combine results from different querysets from SAME model using normal pipe
        #https://groups.google.com/forum/#!topic/django-users/0i6KjzeM8OI
        #If the querysets are from different models, have to use itertools
        #http://chriskief.com/2015/01/12/combine-2-django-querysets-from-different-models/
        #allnotes = allnotes | Note.objects.filter(tag__title__iexact=p) # can have duplicates ... need another method
        
    #http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    # Turn list of values into list of Q objects
    queries = [Q(pricerange__title__iexact=value) for value in pieces]
    # Take one Q object from the list
    query = queries.pop()
    # Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item
    print(query)
    # Query the model
    all_books = Book.objects.filter(query).distinct().order_by('genre__title')
    total = all_books.count()
    return render(request, 'bookstore/index.html', {'pieces':pieces, 'bookstore': all_books, 'total': total})
    
def book(request, book_id):
    book = Book.objects.get(id=book_id) 
    return render(request, 'bookstore/book_detail.html', {'book':book})
    
    
class BookList(ListView):
    #https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
    model = Book
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookList, self).dispatch(*args, **kwargs)

    
    def get_queryset(self):
                #self.request.user will contain the "User" object, however,
        #user field in the Note model is an instance of "UserProfile" object
        #So need to ensure that when we filter all the user owned notes, we
        #filter using the 'correct' UserProfile instance based on logged in "User" object 
        #in self.request.user
        curruser = UserProfile.objects.get(user=self.request.user)

        genre = self.kwargs['genre']
        if genre == '':
            #filter based on current logged in user
            self.queryset = Book.objects.filter(user=curruser)

            return Book.objects.all()
        else:
            #filter based on current logged in user
            self.queryset = Book.objects.all().filter(user=curruser).filter(genre__title__iexact=genre)

            return Book.objects.filter(genre__title__iexact=genre)

    def get_context_data(self, **kwargs):
        context = super(NoteList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        #provided so that the avatar can be displayed in base.html
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
