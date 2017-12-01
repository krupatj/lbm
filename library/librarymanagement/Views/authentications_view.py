from rest_framework import serializers
import datetime
from django.views import View
from django.http import HttpResponse
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from librarymanagement.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from ..forms import AddAuthorForm,AddBookForm


        

class Authentication(View):
    def post(self, request):
        """
        purpose: Creates a new account for the user who has signed up
        Input:None
        Returns:goes back to signup page after account creation
        """
        form = UserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
          
            messages.info(request, 'new account Created')
            return HttpResponseRedirect('/admin_index/')
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect('/basepage/')

    def get(self, request):
       form = UserCreationForm()
       return render(request, 'librarymanagement/base_page.html', {'form': form})

class LoginView(View):

 

    def post(self,request):

        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            """
            Purpose: Adds the user who has logged in to the model CusomUsers if the
            user is not present in the Custommodel users list
            """
            id_list = CustomUsers.objects.values('user_id')
            reg_id = [values['user_id'] for values in id_list]
            flag = 'false'
            for search_id in reg_id:
                if search_id == request.user.id:
                    flag = 'true'
            if flag == 'false':
                new_user = CustomUsers(user_id=request.user.id)
                new_user.save()
            else:
                print("User already exists!!")
            if  user.is_superuser:
                return HttpResponseRedirect('/admin_index/')
            else:
                return HttpResponseRedirect('/user_index/')
        else:
            messages.error(request, 'Invalid Credentials')
            return HttpResponseRedirect('/signup/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_index(request):
    """Purpose: Takes the logged in user to the admin home page if the user is a superuser
    Input:none
    Returns:admin is redirected to admin homepage"""
    if  not request.user.is_authenticated:
        return HttpResponseRedirect('/signup/')
    user = request.user.first_name
    return render(request, 'librarymanagement/admin_index.html', {'user':user})


class LogoutView(View):

    def get(self,request):
        logout(request)
        messages.info(request, 'Successfully logged out')
        return HttpResponseRedirect('/basepage/')