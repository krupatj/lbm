from django.db import models
from django import forms
import datetime
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
DECISION_CHOICES = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject'),
        ('On Hold', 'On Hold')
    )
RETURN_STATUS_CHOICES = (
        ('Received', 'Received'),
        ('Not Received', 'Not Received')
    )
CHANGE_STATUS = (
        ('Received', 'Received'),
        ('Not Received', 'Not Received')
    )


class CustomUsers(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list

    def __str__(self):
        return self.user.username

class Author(models.Model):
    first_name = models.CharField(max_length=30,)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    country= models.CharField(max_length=30)
    photo = models.ImageField(upload_to='authors', null= True,blank= True)
    
    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)
        
class Book(models.Model):
    book_title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author', related_name="authors")
    description = models.TextField(blank=True, null=True)
    stock_count = models.IntegerField()

    def __str__(self):
        return self.book_title

class Review(models.Model):
    user = models.ForeignKey(CustomUsers, null=False, related_name="review")
    book = models.ForeignKey(Book, null=True, related_name="reviews")
    book_title = models.CharField(max_length=30,blank=True)
    review = models.TextField(max_length=300)
    
    def __str__(self):
        return self.book_title

class Photo(models.Model):
    photo = models.ImageField(upload_to='books', null=True,blank=True)
    book = models.ForeignKey(Book, null=True, related_name="photos")
    book_title = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.book_title

class LendRequest(models.Model):
    user = models.ForeignKey(CustomUsers, null=False, related_name="lendrequests")
    book = models.ManyToManyField(Book, related_name="books")
    date = models.DateTimeField(default=datetime.datetime.now() , blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    final_decision = models.CharField(max_length=10, choices=DECISION_CHOICES)

   
    def __str__(self):
        return self.status

class ReturnRequest(models.Model):
    user = models.ForeignKey(CustomUsers, null=False, related_name="user_return")
    book = models.ManyToManyField(Book, related_name="book_return")
    date = models.DateTimeField(default=datetime.datetime.now() , blank=False)
    return_status = models.CharField(max_length=30, choices=RETURN_STATUS_CHOICES)
    change_status = models.CharField(max_length=30, choices=CHANGE_STATUS)

    def __str__(self):
       return self.return_status