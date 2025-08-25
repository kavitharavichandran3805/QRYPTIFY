from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.models import Session 
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
# from rest_framework_simplejwt.tokens import RefreshToken

def get_csrf_token(request):
    return JsonResponse({"token":get_token(request)})
class LoginAPI(APIView):

    def get(self,request):
        users_obj=User.objects.all()
        if not users_obj.exists():
            return Response({"status":False,"message":"No user exists"},status=status.HTTP_404_NOT_FOUND)
        serializers=UserSerializer(users_obj,many=True)
        return Response({"status":True,"data":serializers.data},status=status.HTTP_200_OK)

    def post(self,request):
        data=request.data
        email = data.get('email')
        password = data.get('password')
        print(email,password)
        print("inside the login api")

        if not email or not password:
            return Response(
                {"status": False, "message": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status":False,"message":"User does not exits"},status=status.HTTP_404_NOT_FOUND)
        user=authenticate(username=user.username,password=password)
        if user is not None:
            login(request,user)
            return Response({"status":True,"message":"Successfully logged in"},status=status.HTTP_200_OK)
        return Response({"status":False,"message":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        data = request.data
        email = data.get('email')
        try:
            obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": False, "message": "No user exists"}, status=status.HTTP_404_NOT_FOUND)
        password = data.get('password')
        if password:
            obj.set_password(password) 
            obj.save()
            return Response({"status": True, "message": "Password updated successfully"})
        serializer = UserSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Successfully updated"})
        
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request):
        data=request.data
        email=data.get('email')
        user=User.objects.filter(email=email)
        user.delete()
        return Response({"status":True,"message":"Successfully deleted"})

class SignupAPI(APIView):

    def post(self,request):
        data=request.data
        serializers=UserSerializer(data=data)
        if not serializers.is_valid():
            return Response({"status":False,"message":serializers.errors},status=status.HTTP_400_BAD_REQUEST)
        user=serializers.save()
        login(request,user)
        return Response({"status":True,"message":"Successfully signed in"},status=status.HTTP_201_CREATED)
    
class UserDetailsAPI(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            user=request.user
            return Response({
                'status': True,
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status':False,
                'message':'User is not authenticated'
            },status=status.HTTP_401_UNAUTHORIZED)



