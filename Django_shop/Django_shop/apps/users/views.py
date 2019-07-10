from django.shortcuts import render

# Create your views here.
from rest_framework import status
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

class VerifyEmailView(APIView):

    def get(self,request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message':'缺少token'},status=status.HTTP_400_BAD_REQUEST)

        user = User.check_verify_email_token(token)

        if user is None:
            return Response({"message":"链接信息无效"},status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({"message":"ok"})