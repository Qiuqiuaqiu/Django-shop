from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from users.serializers import EmailSerializer
from . import serializers
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serilaizers import CreateUserSerializer


class UsernameCountView(APIView):

    def get(self,request,username):

        count = User.objects.filter(username=username).count()

        data = {
            "username": username,
            "count": count
        }
        return Response(data)

class MobileCountView(APIView):

    def get(self,request,mobile):

        count = User.objects.filter(mobile=mobile).count()

        data = {
            "mobile": mobile,
            "count": count
        }

        return Response(data)

class UserView(CreateAPIView):

    serializer_class = CreateUserSerializer

class UserDetailView(RetrieveAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class EmailView(UpdateAPIView):

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

