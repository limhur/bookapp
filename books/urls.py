from django.conf.urls import patterns, include, url
from django.contrib import admin
from bookstore import views
from django.views.generic import ListView
from bookstore.models import Book
from django.conf.urls import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^list/$', views.BookList.as_view(), name='books_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/(?P<book_id>\d+)$', views.book, name='book_detail'),
    url(r'^genre/(?P<genre>.*)$', views.bookstore_list, name='bookstore_list'),
    url(r'^author/(?P<author>.*)$', views.bookstore_author, name='bookstore_list'),
    url(r'^listall/$', ListView.as_view(model=Book), name = 'listall'),
    url(r'^list/(?P<genre>.*)$', views.BookList.as_view(), name='bookstore_list'),
    url(r'^detail/(?P<book_id>\d+)$', views.book, name='detail'), 
    #url(r'^add/$', views.BookCreate.as_view(), name='book_add'),
    url(r'^book/(?P<pk>\d+)/edit/$', views.BookUpdate.as_view(),  name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(),  name='book_delete'),
    url(r'^add/$', views.MyView.as_view(), name="book_add"),

    url(r'^book/(?P<pk>\d+)$', views.BookDetail.as_view(),  name='detail'),
    url(r'^accounts/', include('accounts.urls')),
    
)





    

