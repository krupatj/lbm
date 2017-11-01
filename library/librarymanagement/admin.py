from django.contrib import admin
from django.contrib.auth.models import User
from .models import User,Author, Review, Photo, Book, LendRequest,ReturnRequest,CustomUsers

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Photo)
admin.site.register(LendRequest)
admin.site.register(ReturnRequest)
admin.site.register(CustomUsers)

