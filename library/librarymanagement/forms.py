from django import forms
from .models import Author,Book,Photo
from django.forms.models import model_to_dict, fields_for_model

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name','age', 'country', 'photo')


class AddBookForm(forms.ModelForm):
    photo = forms.ImageField(label='book_image', max_length=100)
    class Meta:
        model = Book
        fields = ('book_title','authors','description', 'stock_count')

