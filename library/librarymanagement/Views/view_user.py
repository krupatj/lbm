import datetime
from django.views.generic import *
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from librarymanagement.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from ..forms import AddAuthorForm,AddBookForm


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_index(request):
    """
    Purpose: Takes the logged in user to the user homepage
    Input:None
    Returns:user redireded to user home page
    """
    if  not request.user.is_authenticated:
    	
        return HttpResponseRedirect('/signup/')
    user = request.user.first_name
    return render(request, 'librarymanagement/user_index.html', {'user':user})


class UserRequestsView(View):

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def user_lend_list(request):
        """Purpose: Displays a list of lend requests made by he user who is logged in
           Input:None
           Returns:Redirects the client_list
        """
        if request.user.is_authenticated:
            user_id_base =  request.user.id
            id = CustomUsers.objects.get(user_id=user_id_base).pk
            lend_list = LendRequest.objects.filter(user_id=id,status__in=['Pending','Rejected']).order_by("user_id")
            count = 8
            lends = pagination(request, count, lend_list)
            return render(request, 'librarymanagement/client_lend_list.html', {'lend_list':lends})
        else:
            return HttpResponseRedirect('/signup/')

    
    def user_borrowed_books_list(request):
        """Purpose: Displays a list of borrow requests made by the user who is logged in
           Input:None
           Returns:Redirects the borrowed book list page
        """
        if  not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')
        user_id_base =  request.user.id
        user_id = CustomUsers.objects.get(user_id=user_id_base).pk
        borrowed_book_list = LendRequest.objects.filter(user_id=user_id,final_decision='Approved',status='Approved').order_by('status') 
        count = 5
        books = pagination(request,count,borrowed_book_list)
        return render(request, 'librarymanagement/user_borrowed_books.html', {'book_list':
            books})

    
    def user_return_list(request):
        """Purpose:Displays the return requests made by the user who is logged in
           Input :none
           return:client_return_list.html page is rendered
        """
        if  not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')
        user_id_base =  request.user.id
        id = CustomUsers.objects.get(user_id=user_id_base).pk
        return_list = ReturnRequest.objects.filter(user_id=id, review_status='Not Complete').order_by('book')
        #pagination code to display 10 entries per page
        count = 5
        returns = pagination(request,count,return_list)
        return render(request, 'librarymanagement/client_return_list.html', {'return_list':returns})


class UserActionsView(View):

    def user_lend_book(request,requested_book_id):
        """Purpose: Enables the user to make a lend request
           Input:return_book_id
           Returns:Redirects the book list page
        """
        if  not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')

        final_user_id = CustomUsers.objects.get(user_id=request.user.id).pk
        book = Book.objects.get(id=requested_book_id)
        lend_list = LendRequest.objects.filter(user_id=final_user_id,status='Pending',book =requested_book_id )
        print (lend_list)
        if not lend_list :
            print("-------------")
            print ("no prior requests!!")
            if not book.stock_count == 0:
                lend_request = LendRequest(user_id=final_user_id,date=datetime.datetime.now(),
                                       status='Pending',final_decision='On Hold')
                lend_request.save()
                lend_request.book.add(requested_book_id)
                lend_request.save()
            else:
               #messages.info(request, 'Couldnt make the request..Empty Stock!!')
               return HttpResponseRedirect('/books_list/')   
        else:   
            print("-------------")
            #messages.info(request, 'You have already made a request for the book!')
            return HttpResponseRedirect('/books_list/') 
              
    def user_return_book(request, return_book_id, lend_id):
        """Purpose: Enables the user to make a return request
           Input:return_book_id
           Returns:Redirects the borrowed book list page
        """
        if  not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')

        lend_data = LendRequest.objects.get(id=lend_id)
        print (lend_data.status)
        lend_data.status = 'Return_requested'
        lend_data.save()
        book_to_return = return_book_id
        user_id_base = request.user.id
        final_user_id = CustomUsers.objects.get(user_id=user_id_base).pk
        return_request = ReturnRequest(user_id=final_user_id,date=datetime.datetime.now(),
                         return_status='Not Received',change_status='Not Received')
        return_request.save()
        return_request.book.add(book_to_return)
        return HttpResponseRedirect('/userborrowedbookslist/')


    def user_write_review(request, book_id, return_id):
        """Purpose:Redirects to a new page to write a review about a book
           Input :book_id
           return:user_write_review.html page is rendered
        """
        if  not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')
        return render(request, 'librarymanagement/user_write_review.html', {'book_id':book_id, 'return_id':return_id})


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def user_submit_review(request, book_id, return_id):
        """Purpose:User writes a revoew about a book if the return request is approved by the admin
           Input:book_id of thebook for which the review is made
           Return:rediretced to return userreturnlsit view
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')
        return_request = ReturnRequest.objects.get(id=return_id)
        return_request.review_status = 'Complete'
        return_request.save()
        user_id_base = request.user.id
        final_user_id = CustomUsers.objects.get(user_id=user_id_base).pk
        review_content = request.POST.get('review_content', '')
        book_title = Book.objects.get(id=book_id)
        review = Review(user_id=final_user_id, book_id=book_id, book_title=book_title,
                        review=review_content)
        review.save()
        return HttpResponseRedirect('/userreturnlist/')


def pagination(request,count, data_list):
    """
    Purpose: Displays only a specific number of items in a single page
    Input:count of items to be displayed
    Returns: redirected to return requestview
    """
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
