from rest_framework import generics
from django.shortcuts import render


class Registration(generics.GenericAPIView):

    def post(self, request):
        user = request.data
