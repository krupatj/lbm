from django.shortcuts import render
import datetime
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from librarymanagement.models import Book, Author, LendRequest, ReturnRequest, DECISION_CHOICES, CHANGE_STATUS, Photo,  Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages



def user_index_new(request):
    """
    Purpose: Takes the logged in user to the user homepage
    Input:None
    Returns:user redireded to user home page
    """
    user = request.user
    return render(request, 'librarymanagement/user_index.html', {'user':user})

def books_new(request):
    """Purpose: Displays a list of books with relevant details
       Input:None
       Returns:redirected to the page displyaing  list of books  
    """
    base_page = "librarymanagement/user_index.html"
    print("%s in books page " %(request.user))
    books_list = Book.objects.order_by("book_title")
    authors_list = Author.objects.all()
    count = 2
    books = pagination(request,count,books_list)
    print (books)
    return render(request, 'librarymanagement/books2.html',
        {'books_info':books, 'authors_list':authors_list, "base_page": base_page})
        



def book_details_new(request,books_id):
    """Purpose: Displays the details of a specific book 
       Input:book_id of the book which the user has clicked
       Returns:Renders the book_detail page 
    """
    print("%s in book_detail page " %(request.user))
    print(books_id)
    base_page = "librarymanagement/user_index.html"
    if request.user.is_superuser:
        base_page = "librarymanagement/index.html"
    book = Book.objects.get(pk=books_id)
    authors_list = Author.objects.order_by("first_name")
    return render(request, 'librarymanagement/book_details.html', 
                 {'book':book, 'authors_list':authors_list, "base_page": base_page})


def pagination(request,count, data_list):
    """
	Purpose: Displays only a specific number of items in a single page
    Input:count of items to be displayed
    Returns: redirected to return requestview
    """
    print(request.user)
    print(count,)
    print("-------------")
    print(data_list)
    paginator = Paginator(data_list, count)
    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authors = paginator.page(paginator.num_pages)
    return (authors)

