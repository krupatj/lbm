import datetime
from django.http import HttpResponse
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from librarymanagement.models import Book, Author, LendRequest, ReturnRequest, DECISION_CHOICES, CHANGE_STATUS, Photo, CustomUsers, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from ..forms import AddAuthorForm,AddBookForm
from django.shortcuts import render_to_response
from .authentications_view import *
from .view_user import pagination

def set_index_page(request):
    """
        Purpose: sets the index page depending upin the user who has logged in!
        Input:None
        Returns:link of index page"""
    if not request.user.is_superuser:
        base_page = 'librarymanagement/user_index.html'
        return (base_page)
    base_page = 'librarymanagement/admin_index.html'
    return (base_page)

class BookList(ListView):
    """
    Purpose: Displays a list of books with relevant details
    Input:None
    Returns:redirected to the page displyaing  list of books"""

    model = Book
    context_object_name  = 'books_info'
    queryset = Book.objects.order_by('book_title')
    template_name = 'librarymanagement/books_class.html'
    books_list = queryset

    def get_context_data(self, **kwargs):
        
        context = super(BookList, self).get_context_data(**kwargs)
        context['authors_list'] = Author.objects.all()
        base_page = set_index_page(self.request)
        context['base_page'] = base_page
        queryset = Book.objects.order_by('book_title')
        template_name = 'librarymanagement/books_class.html'
        books_list = queryset
        count = 2
        books = pagination(self.request,count,books_list)
        context['books_info'] = books
        return context

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def add_book(request):
        """Purpose: Allows the admin to create a new book
           Input:None
           Returns:Renders the books page 
        """
        base_page = 'librarymanagement/admin_index.html'
        if  not request.user.is_authenticated:
            next_page = '/signup/'
       
        if request.method == 'POST':
            form = AddBookForm(request.POST,request.FILES)
            book_image = request.FILES.get('photo')
            if form.is_valid():
                validated_form = form.save()
                photo = Photo(photo=book_image, book_title=validated_form.book_title, book_id=validated_form.pk)
                photo.save()
                next_page = '/books_list/'
                #return HttpResponseRedirect('/books_list/')
            else:
               errors = form.errors
               messages.info(request, form.errors)
               next_page = '/books_list/'
               #return HttpResponseRedirect('/books_list/')
        return HttpResponseRedirect(next_page)
        

class BookDetailsView(DetailView):
    """Purpose: Displays the details of a specific book 
       Input:book_id of the book which the user has clicked
       Returns:Renders the book_detail page 
    """

    model = Book
    context_object_name  = 'book'
    template_name = 'librarymanagement/book_details_class.html'
   
    def get_context_data(self, **kwargs):
        context = super(BookDetailsView, self).get_context_data(**kwargs)
        context['authors_list'] = Author.objects.order_by("first_name")
        base_page = set_index_page(self.request) 
        context['base_page'] = base_page
        return context


class LendRequestView(View):
    """Purpose: Displays a list of lend requests made by all the users
       Input:None
       Returns:Redirects the lend request page
    """
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if  not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
       
        decision = DECISION_CHOICES
        lend_list = LendRequest.objects.filter(status__in=['Pending','Rejected']).order_by("user")
        count = 5
        lends = pagination(request,count,lend_list)
        return render(request, 'librarymanagement/lendrequest.html', {'lend_list':lends, 'decision':decision})

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def approve_lend_request(request, lend_id):
        """Purpose: Admin can approve a lend request made by a user
            Input:lend_id
            Returns:Redirects the lend_request view
        """
        if  not request.user.is_superuser:
            
            return HttpResponseRedirect('/signup/')
        if request.method == 'POST':
            
            lender = LendRequest.objects.get(pk=lend_id)
            for book in lender.book.all():
                if book.stock_count == 0:
                    messages.error(request, 'Empty Stock!, Cannot approve request :( ')
                    lender.final_decision = 'Rejected'
                    book.save()
                else:
                    lender.final_decision = 'Approved'
                    book.stock_count = book.stock_count - 1
                    book.save()
            # Changes the value too status if it is not equal to final decision value
            if lender.status != lender.final_decision:
                lender.status = lender.final_decision
            lender.save()
            return HttpResponseRedirect('/lendrequests/')

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def reject_lend_request(request, lend_id):
        """Purpose:Admin can reject a lend request made by a user
            Input:lend_id of the lend request
            Returns:Redirects the lendrequest view
        """
        if  not request.user.is_superuser:
            next_page = '/signup/'
            #return HttpResponseRedirect('/signup/')

        if request.method == 'POST':
            lender = LendRequest.objects.get(pk=lend_id)
            lender.final_decision = 'Rejected'
            # Changes the value to status if it is not equal to final decision value
            if lender.status != lender.final_decision:
                lender.status = lender.final_decision
            lender.save()
            next_page = '/lendrequests/'
            #return HttpResponseRedirect('/lendrequests/')
        else:
            next_page = '/signup/'
            #return HttpResponseRedirect('/signup/')
        return HttpResponseRedirect(next_page)
        
class BorrowedBooksView(View):
    """Purpose: Displays a list of borrow requests made by all users 
        Input:None
        Returns:Redirects the  book list page
    """
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def borrowed_books_list(request):
        """Purpose: Displays a list of borrow requests made by all users
           Input:None
           Returns:Redirects the borrowed book list page
        """
        if  not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
        borrowed_book_list = LendRequest.objects.filter(final_decision='Approved',status='Approved').order_by("user_id")
        count = 5
        books = pagination(request,count,borrowed_book_list)
        return render(request, 'librarymanagement/admin_borrowed_books_list.html', {'book_list':books})



class ReturnRequestView(View):
    """Purpose:displays the return requests made by the users
       Input :none
       return:returnrequest.html page is rendered
    """
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
        decision = CHANGE_STATUS
        return_list = ReturnRequest.objects.filter(return_status='Not Received')
        #pagination code to display 4 entried per page
        count = 10
        returns = pagination(request,count,return_list)
        return render(request, 'librarymanagement/returnrequest.html', 
            {'return_list':returns,'decision':decision})


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def approve_return_request(request, return_id):
        """Purpose:Enables the admin to approve a return request made by the users
           Input:return_id of the return requests
           Return:rediretced to return request view
        """
        if  not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
        if request.method == 'POST':
            lender = ReturnRequest.objects.get(pk=return_id)
            lender.change_status = 'Received'
            for book in lender.book.all():
                book.stock_count = book.stock_count + 1
                book.save()
            if lender.return_status != lender.change_status:
                lender.return_status = lender.change_status
            lender.save()
            return HttpResponseRedirect('/returnrequests/')
        else:
            return HttpResponseRedirect('/signup/')


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def reject_return_request(request, return_id):
        """Purpose:Enables the admin to reject a return request made by the users
            Input:return_id, id of the return request
            Returns: redirected to return requestview
        """
        if  not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
        if request.method == 'POST':
            lender = ReturnRequest.objects.get(pk=return_id)
            lender.change_status = ' Not Received'
            if lender.return_status != lender.change_status:
                lender.return_status = lender.change_status
            lender.save()
            return HttpResponseRedirect('/returnrequests/')
    

class AuthorView(View):

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        """
        Displays the list of authors with necessary details 
        Input:None
        Returns:Redirects the authors page displaying list of authors
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')
        authors_list = Author.objects.order_by("first_name")
        count = 8
        authors = pagination(request,count,authors_list)
        base_page = "librarymanagement/user_index.html"
        if request.user.is_superuser:
            base_page = "librarymanagement/admin_index.html"
        return render(request, 'librarymanagement/authors.html', {'author_info':authors, "base_page": base_page})
       

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def add_author(request):
        """Purpose: Allows the admin to addan author
           Input:None
           Returns:Redirects the authors page
        """
        if  not request.user.is_superuser:
            return HttpResponseRedirect('/signup/')
        if  not request.method == 'POST':
            return render(request, 'librarymanagement/authors.html')
        form = AddAuthorForm(request.POST, request.FILES)
        if not  form.is_valid():
            errors = form.errors
            messages.info(request, form.errors)
            return HttpResponseRedirect('/authors/')
        form.save()
        messages.info(request, 'author Successfully added!!! ')
        return HttpResponseRedirect('/authors/')