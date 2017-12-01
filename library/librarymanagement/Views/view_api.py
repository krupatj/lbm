from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Book
from ..serializers1 import bookSerialzers

class BookList(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        serializer = bookSerialzers(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
    	return Book.objects.all()
    
    def post(self, request):
        pass




