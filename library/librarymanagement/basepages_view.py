import datetime
from django.http import HttpResponse
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from librarymanagement.models import Book, Author, LendRequest, ReturnRequest, DECISION_CHOICES, CHANGE_STATUS, Photo,Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from ..forms import AddAuthorForm,AddBookForm
from django.shortcuts import render_to_response

class BasePage(TemplateView):
    """
    Purpose:renders the base page which contains the signup and login options
    Input:None
    Returns:Renders the base_page 
    """
    template_name = 'librarymanagement/base_page.html'