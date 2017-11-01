from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from librarymanagement.models import Book,Author,LendRequest,ReturnRequest,DECISION_CHOICES,CHANGE_STATUS,Photo,CustomUsers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddAuthorForm,AddBookForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import template


def basepage(request):
    return render(request, 'librarymanagement/base_page.html')


def signup(request):
    print ("%s at the signup page " %(request.user))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account_created/')
    else:
        form = UserCreationForm()
    return render(request, 'librarymanagement/base_page.html', {'form': form})


def account_created(request):
     return HttpResponseRedirect('/signup/')

def login_window(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    print ('user', user)
    
    if user is not None:
        login(request, user)
        if user.is_superuser:
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponseRedirect('/user_index/')
    return HttpResponseRedirect('/signup/')

@login_required
def logout_window(request):
    print('At the logout view')
    print ("%s logging out" %(request.user))
    logout(request)
    print('Logout success!')
    return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        return render(request, 'librarymanagement/index.html')
    else:
        return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_index(request):
    if request.user.is_authenticated:
        return render(request, 'librarymanagement/user_index.html')
    else:
        return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def books(request):
    
    if request.user.is_authenticated:
        print ("%s in books page " %(request.user))
        books_list = Book.objects.order_by("book_title")
        authors_list = Author.objects.all()
        paginator = Paginator(books_list, 2)
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)
        return render(request, 'librarymanagement/books2.html',{'books_info':books,'authors_list':authors_list})
    else:
        print ("%s attempted to access books " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def book_details(request,books_id):

    if request.user.is_authenticated:
       print ("%s in book_detail page " %(request.user))
       print (books_id)
       book = Book.objects.get(pk=books_id)
       authors_list = Author.objects.order_by("first_name")
       return render(request, 'librarymanagement/book_details.html', {'book':book,'authors_list':authors_list})
    else:
       
        print ("%s attempted to access book_detail page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_book(request):
    if request.user.is_authenticated:
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
                print (photo)
                return HttpResponseRedirect('/books/')
            else:
                print (form.errors)
                return render(request,'librarymanagement/books2.html')
        else:
            return render(request, 'librarymanagement/books2.html')
    else:
        print ("%s attempted to access book_add page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def authors(request):
    """
    Auhors view
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
    if request.user.is_authenticated:
        print ("%s in add author page " %(request.user))
        if request.method == 'POST':
            form = AddAuthorForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return render(request,'librarymanagement/add_author.html',{'form': form})
            else:
                errors = form.errors
                return render(request, 'librarymanagement/error_page.html',{'errors':errors} )
        else:
            return render(request, 'librarymanagement/authors.html')
    else:
        print ("%s attempted to access add_author page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approve_request(request):
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
        else:

            return HttpResponseRedirect('/signup/')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lend_request(request):
    if request.user.is_superuser:

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
    else:
        print ("%s attempted to access lend_request page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_lend_list(request):
    if request.user.is_authenticated:
        print ("%s in client_lend_list page " %(request.user))
        print("----------------------")
        user_id_base =  request.user.id
        print("----------------------")
        print ("The actual user Id from auth.users",user_id_base)
        id = CustomUsers.objects.get(user_id=user_id_base).pk
        print("----------------------")
        print ("id from custom users", id)
        print("----------------------")
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
def approve_lend_request(request, lend_id):
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
            if lender.status != lender.final_decision:
               lender.status = lender.final_decision
            lender.save()
            print ("status changed to %s " %(lender.final_decision))
            return HttpResponseRedirect('/lendrequest/')
        else:
            print ("%s attempted to access approve_lend_request page " %(request.user))
            return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject_lend_request(request, lend_id):
        if request.method == 'POST':
            print (request.user)
            print("request_rejected")
            lender = LendRequest.objects.get(pk=lend_id)
            lender.final_decision = 'Rejected'

            if lender.status != lender.final_decision:
               lender.status = lender.final_decision
            lender.save()
            print ("status changed to %s " %(lender.final_decision))
            return HttpResponseRedirect('/lendrequest/')
        else:
            return HttpResponseRedirect('/signup/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_request(request):
    if request.user.is_superuser:
        print ("%s in return_request page " %(request.user))
        decision = CHANGE_STATUS
        print (request.user)
        return_list = ReturnRequest.objects.order_by("user")

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
    else:
        print ("%s attempted to access return_request page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_return_list(request):
    if request.user.is_authenticated:
        print("----------------------------------------------")
        print ("%s in user_return_list page " %(request.user))
        print("----------------------------------------------")
        user_id_base =  request.user.id
        print ("The actual user Id from auth.users",user_id_base)
        id = CustomUsers.objects.get(user_id=user_id_base).pk
        print("----------------------")
        print ("id from custom users", id)
        print("----------------------")
        return_list = ReturnRequest.objects.filter(user_id=id)

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
    else:
        print ("%s attempted to access user_return_list page " %(request.user))
        return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approve_return_request(request, return_id):
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
        else:
           return HttpResponseRedirect('/signup/')
