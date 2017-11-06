from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from librarymanagement.models import Book,Author,LendRequest,ReturnRequest,DECISION_CHOICES,CHANGE_STATUS,Photo,CustomUsers,Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddAuthorForm,AddBookForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import template
import datetime


def basepage(request):
    """
    Purpose:renders the base page which contains the signup and login options
    Input:None
    Returns:Renders the base_page 
    """
    return render(request, 'librarymanagement/base_page.html')


def signup(request):
    """
    purpose: Creates a new account for the user who has signed up
    Input:None
    Returns:goes back to signup page after account creation
    """
    print ("%s at the signup page " %(request.user))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print (request.POST)
        if form.is_valid():
            print(request.user)
            form.save()
            print(request.user.id)
            return HttpResponseRedirect('/signup/')
    else:
        form = UserCreationForm()
    return render(request, 'librarymanagement/base_page.html', {'form': form})

def login_window(request):
    """
    Purpose:Does the authentication of the user who has attempted o login
    Input:None
    Returns:Renders the user_index or admin_index page depending on whether the user is admin or not 
    """
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    print ('user', user)
    
    if user is not None:
        login(request, user)
        """
        Purpose: Adds the user who has logged in to the model CusomUsers if the
        user is not present in the Custommodel users list
        """
        id_list = CustomUsers.objects.values('user_id')
        print("___________")
        print ("Value of userid in CustomUsers")
        reg_id = [values['user_id'] for values in id_list]
        print (reg_id)
        flag = 'false' 
        for search_id in reg_id:
            print ("id of logged user is ",request.user.id, "search id is ",search_id)
            if search_id == request.user.id:
                flag = 'true'
        if flag == 'false':
            new_user = CustomUsers(user_id=request.user.id)
            new_user.save()
            print("New User Added to CustomUsers!!")
        else:
            print("User already exists!!")

        if  user.is_superuser:
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponseRedirect('/user_index/')
    else:
        return HttpResponseRedirect('/signup/')

@login_required
def logout_window(request):
    """Purpose: Logs out the user 
       Input:None
       Returns:user is redirected to the signup page
    """
    print('At the logout view')
    print ("%s logging out" %(request.user))
    logout(request)
    print('Logout success!')
    return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    """
    Purpose: Takes the logged in user to the admin home page if the user is a superuser
    Input:none
    Returns:admin is redirected to admin homepage
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signup/')
    user = request.user.first_name
    return render(request, 'librarymanagement/index.html',{'user':user})

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
    return render(request, 'librarymanagement/user_index.html',{'user':user})
       
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def books(request):
    """Purpose: Displays a list of books with relevant details
       Input:None
       Returns:redirected to the page displyaing  list of books  
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access books " %(request.user))
        return HttpResponseRedirect('/signup/')

    print ("%s in books page " %(request.user))
    books_list = Book.objects.order_by("book_title")
    authors_list = Author.objects.all()
    paginator = Paginator(books_list, 2)
    page = request.GET.get('page')
    base_page = "librarymanagement/user_index.html"
    if request.user.is_superuser:
        base_page = "librarymanagement/index.html"
    #Purpose: Pagination code to display 2 books per page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    return render(request, 'librarymanagement/books2.html',
        {'books_info':books,'authors_list':authors_list,"base_page": base_page})
        


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def book_details(request,books_id):
    """Purpose: Displays the details of a specific book 
       Input:book_id of the book which the user has clicked
       Returns:Renders the book_detail page 
    """
    if not  request.user.is_authenticated:
        print ("%s attempted to access book_detail page " %(request.user))
        return HttpResponseRedirect('/signup/')

    print ("%s in book_detail page " %(request.user))
    print (books_id)
    base_page = "librarymanagement/user_index.html"
    if request.user.is_superuser:
        base_page = "librarymanagement/index.html"
    book = Book.objects.get(pk=books_id)
    authors_list = Author.objects.order_by("first_name")
    return render(request, 'librarymanagement/book_details.html', 
                 {'book':book,'authors_list':authors_list,"base_page": base_page})
        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_book(request):
    """Purpose: Allows the admin to create a new book
       Input:None
       Returns:Renders the books page 
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access book_add page " %(request.user))
        return HttpResponseRedirect('/signup/')
    print ("%s in add_book page " %(request.user))
    if request.method == 'POST':
        print(request.POST)
        form = AddBookForm(request.POST,request.FILES)
        book_image = request.FILES.get('photo')
        if form.is_valid():
            print ("success!")
            validated_form = form.save()
            print ('----------', validated_form.pk)
            photo = Photo(photo=book_image, book_title=validated_form.book_title, book_id=validated_form.pk)
            photo.save()
            return HttpResponseRedirect('/books/')
        else:
            print (form.errors)
            return render(request,'librarymanagement/books2.html')
    else:
        return render(request, 'librarymanagement/books2.html')

        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_lend_book(request,requested_book_id):
    """Purpose: Creates a lend request for a specific book by the user who is logged in
       Input:book_id
       Returns:Redirects to the books page
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access user_lend_book page " %(request.user))
        return HttpResponseRedirect('/signup/')

    book_requested = requested_book_id
    print("book selected to lend is ",requested_book_id)
    user_id_base =  request.user.id
    final_user_id = CustomUsers.objects.get(user_id=user_id_base).pk
    print("----------------------")
    print ("id from custom users", id)
    print("----------------------")
    lend_request = LendRequest(user_id=final_user_id,date=datetime.datetime.now(),status='Pending',final_decision='On Hold')
    lend_request.save()
    lend_request.book.add(requested_book_id)
    return HttpResponseRedirect('/books/')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def authors(request):
    """
    Displays the list of authors with necessary details 
    Input:None
    Returns:Redirects the authors page displaying list of authors
    """
    if request.user.is_authenticated:
        print ("%s in authors page " %(request.user))
        authors_list = Author.objects.order_by("first_name")
        paginator = Paginator(authors_list, 8)
        page = request.GET.get('page')
        base_page = "librarymanagement/user_index.html"
        if request.user.is_superuser:
            base_page = "librarymanagement/index.html"
        try:
            authors = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            authors = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            authors = paginator.page(paginator.num_pages)
        return render(request, 'librarymanagement/authors.html',{'author_info':authors, "base_page": base_page})
    else:
        print ("%s attempted to access authors page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_author(request):
    """Purpose: Allows the admin to addan author
       Input:None
       Returns:Redirects the authors page
    """
    if  not request.user.is_superuser:
        print ("%s attempted to access add_author page " %(request.user))
        return HttpResponseRedirect('/signup/')
    print ("%s in add author page " %(request.user))
    if request.method == 'POST':
        print("post success")
        form = AddAuthorForm(request.POST, request.FILES)
        if form.is_valid():
            print("form valid")
            form.save()
            print("author added")
            return HttpResponseRedirect('/authors/')
        else:
            errors = form.errors
            print (errors)
            return render(request, 'librarymanagement/error_page.html',{'errors':errors} )
    else:
        return render(request, 'librarymanagement/authors.html')
        


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approve_request(request):
    """Purpose: Enables the admin to approve a lend request made by a user
       Input:None
       Returns:Redirects the books page
    """
    if  not request.user.is_superuser:
        print ("%s attempted to access approve lend request page " %(request.user))
        return HttpResponseRedirect('/signup/')
    if request.method == 'POST':
        print (request.user)
        form = AddBookForm(request.POST,request.FILES)
        print (request.POST)
        if form.is_valid():
            print ("success!")
            form.save()
            return render(request,'librarymanagement/add_book.html',{'form': form})
        else:
            print (form.errors)
            return render(request,'librarymanagement/books2.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lend_request(request):
    """Purpose: Displays a list of lend requests made by all the users
       Input:None
       Returns:Redirects the lend request page
    """
    if  not request.user.is_superuser:
        print ("%s attempted to access lend_request page " %(request.user))
        return HttpResponseRedirect('/signup/')

    print (User.objects.get(pk=1).first_name)
    print ("%s in lend_request page " %(request.user))
    decision = DECISION_CHOICES
    lend_list = LendRequest.objects.order_by("user")

    paginator = Paginator(lend_list, 4)
    page = request.GET.get('page')
    try:
        lends = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lends = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lends = paginator.page(paginator.num_pages)
    return render(request, 'librarymanagement/lendrequest.html',{'lend_list':lends, 'decision':decision})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_lend_list(request):
    """Purpose: Displays a list of lend requests made by he user who is logged in
       Input:None
       Returns:Redirects the client_list
    """
    if request.user.is_authenticated:
        print("_"*30)
        print ("%s in client_lend_list page " %(request.user))
        print("_"*30)
        user_id_base =  request.user.id
        print("_"*30)
        print ("The actual user Id from auth.users",user_id_base)
        id = CustomUsers.objects.get(user_id=user_id_base).pk
        print("_"*30)
        print ("id from custom users", id)
        print("_"*30)
        lend_list = LendRequest.objects.filter(user_id=id)
        paginator = Paginator(lend_list, 4)
        page = request.GET.get('page')
        try:
            lends = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            lends = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            lends = paginator.page(paginator.num_pages)
            
        return render(request, 'librarymanagement/client_lend_list.html',{'lend_list':lends})
    else:
        print ("%s attempted to access client_lend_list page " %(request.user))
        return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_borrowed_books_list(request):
    """Purpose: Displays a list of borrow requests made by the user who is logged in
       Input:None
       Returns:Redirects the borrowed book list page
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access borrowed_book_list page " %(request.user))
        return HttpResponseRedirect('/signup/')
    user_id_base =  request.user.id
    id = CustomUsers.objects.get(user_id=user_id_base).pk
    print("_"*60)
    print ("id from custom users", id)
    print("_"*60)
    borrowed_book_list = LendRequest.objects.filter(user_id=id,final_decision='Approved')
    paginator = Paginator(borrowed_book_list, 2)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        book_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        book_list = paginator.page(paginator.num_pages)
    return render(request, 'librarymanagement/user_borrowed_books.html',{'book_list':book_list})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_return_book(request,return_book_id):
    """Purpose: Enables the user to make a return request
       Input:return_book_id
       Returns:Redirects the borrowed book list page
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access user_return_book page " %(request.user))
        return HttpResponseRedirect('/signup/')
    book_to_return = return_book_id
    print("book selected to return is ",book_to_return)
    user_id_base =  request.user.id
    print("_"*20)
    print ("The actual user Id from auth.users",user_id_base)
    final_user_id = CustomUsers.objects.get(user_id=user_id_base).pk
    return_request = ReturnRequest(user_id=final_user_id,date=datetime.datetime.now(),
                     return_status='Not Received',change_status='Not Received')
    return_request.save()
    return_request.book.add(book_to_return)
    return HttpResponseRedirect('/userborrowedbookslist/')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approve_lend_request(request, lend_id):
    """Purpose: Admin can approve a lend request made by a user
        Input:lend_id
        Returns:Redirects the lend_request view
    """
    if  not request.user.is_superuser:
        print ("%s attempted to access approve_lend_request page " %(request.user))
        return HttpResponseRedirect('/signup/')
    if request.method == 'POST': 
        print (request.user)
        lender = LendRequest.objects.get(pk=lend_id)
        for book in lender.book.all():
            print (book.book_title)
            print(book.stock_count)
            if book.stock_count == 0:
                print(" Empty Stock ")
                print (lender.book)
                lender.final_decision = 'Rejected'
                book.save()
            else:
                print("Request_approved")
                print (lender.book)
                lender.final_decision = 'Approved'
                book.stock_count = book.stock_count - 1
                print(book.stock_count)
                book.save()
        # Changes the value too status if it is not equal to final decision value
        if lender.status != lender.final_decision:
            lender.status = lender.final_decision
        lender.save()
        print ("status changed to %s " %(lender.final_decision))
        return HttpResponseRedirect('/lendrequest/')
       


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject_lend_request(request, lend_id):
        """Purpose:Admin can reject a lend request made by a user
           Input:lend_id of the lend request
        Returns:Redirects the lendrequest view
        """
        if  not request.user.is_superuser:
            print ("%s attempted to access reject_lend_request_request page " %(request.user))
            return HttpResponseRedirect('/signup/')

        if request.method == 'POST':
            print (request.user)
            print("request_rejected")
            lender = LendRequest.objects.get(pk=lend_id)
            lender.final_decision = 'Rejected'
            # Changes the value to status if it is not equal to final decision value
            if lender.status != lender.final_decision:
               lender.status = lender.final_decision
            lender.save()
            print ("status changed to %s " %(lender.final_decision))
            return HttpResponseRedirect('/lendrequest/')
        else:
            return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_request(request):
    """Purpose:displays the return requests made by the users
       Input :none
       return:returnrequest.html page is rendered
    """
    if  not request.user.is_superuser:
        print ("%s attempted to access return_request page " %(request.user))
        return HttpResponseRedirect('/signup/')

    print ("%s in return_request page " %(request.user))
    decision = CHANGE_STATUS
    print (request.user)
    return_list = ReturnRequest.objects.order_by("user")
    #pagination code to display 4 entried per page
    paginator = Paginator(return_list, 4)
    page = request.GET.get('page')
    try:
        returns = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        returns = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        returns = paginator.page(paginator.num_pages)
    return render(request, 'librarymanagement/returnrequest.html',{'return_list':returns,'decision':decision})

        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_return_list(request):
    """Purpose:Displays the return requests made by the user who is logged in
       Input :none
       return:client_return_list.html page is rendered
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access user_return_list page " %(request.user))
        return HttpResponseRedirect('/signup/')
    user_id_base =  request.user.id
    id = CustomUsers.objects.get(user_id=user_id_base).pk
    return_list = ReturnRequest.objects.filter(user_id=id)
    #pagination code to display 4 entried per page
    paginator = Paginator(return_list, 4)
    page = request.GET.get('page')
    try:
        returns = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        returns = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        returns = paginator.page(paginator.num_pages)
    return render(request, 'librarymanagement/client_return_list.html',{'return_list':returns})
        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_write_review(request,book_id):
    """Purpose:Redirects to a new page to write a review about a book
       Input :book_id
       return:user_write_review.html page is rendered
    """
    if  not request.user.is_authenticated:
        print ("%s attempted to access user_write_review page " %(request.user))
        return HttpResponseRedirect('/signup/')
    print (book_id)
    return render(request, 'librarymanagement/user_write_review.html',{'book_id':book_id})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)        
def user_submit_review(request,book_id):
    """Purpose:User writes a revoew about a book if the return request is approved by the admin
       Input:book_id of thebook for which the review is made
       Return:rediretced to return userreturnlsit view
    """
    if not request.user.is_authenticated:
         print ("%s attempted to access user_submit_review page " %(request.user))
         return HttpResponseRedirect('/signup/')
    print("book id is ")
    print (book_id)
    print ("%s in user_submit_review page " %(request.user))
    user_id_base =  request.user.id
    print ("The actual user Id from auth.users",user_id_base)
    final_user_id = CustomUsers.objects.get(user_id=user_id_base).pk
    print ("id from custom users", final_user_id)
    review_content = request.POST.get('review_content','')
    print(review_content)
    book_title = Book.objects.get(id=book_id)
    review = Review (user_id=final_user_id,book_id=book_id,book_title=book_title,review=review_content)
    review.save()
    print (book_title)
    return HttpResponseRedirect('/userreturnlist/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approve_return_request(request, return_id):
    """Purpose:Enables the admin to approve a return request made by the users
       Input:return_id of the return requests
       Return:rediretced to return request view
    """
    if  not request.user.is_superuser:
        return HttpResponseRedirect('/signup/')
    if request.method == 'POST':
        print ("%s in approve_lend page " %(request.user))
        print("request_approved")
        lender = ReturnRequest.objects.get(pk=return_id)
        lender.change_status = 'Received'
        for book in lender.book.all():
            print (book.book_title)
            print(book.stock_count)
            book.stock_count = book.stock_count + 1
            print(book.stock_count)
            book.save()
        if lender.return_status != lender.change_status:
            lender.return_status = lender.change_status
        lender.save()
        print ("status changed to %s " %(lender.change_status))
        return HttpResponseRedirect('/returnrequest/')
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
        print ("%s in reject_return_request page " %(request.user))
        print("request_rejected")
        lender = ReturnRequest.objects.get(pk=return_id)
        lender.change_status = ' Not Received'
        if lender.return_status != lender.change_status:
            lender.return_status = lender.change_status
        lender.save()
        print ("status changed to %s " %(lender.change_status))
        return HttpResponseRedirect('/returnrequest/')
    
           
