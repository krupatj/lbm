from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import employees
from .serializers import employeeSerialzers

class employee_list(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        employee = employees.objects.all()
        serializer = employeeSerialzers(employee, many=True)
        return Response(serializer.data)
 
    def post(self, request):
        pass


class books_list(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        books = Book.objects.all()
        serializer = employeeSerialzers(employee, many=True)
        return Response(serializer.data)
 
    def post(self, request):
        pass
