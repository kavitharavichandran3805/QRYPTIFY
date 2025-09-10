from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from qryptify.settings import DEFAULT_TO_EMAIL1,DEFAULT_TO_EMAIL2,DEFAULT_TO_EMAIL3
from .serializers import UserSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.models import Session 
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from datetime import timedelta
from rest_framework.permissions import AllowAny



def get_csrf_token(request):
    print("inside the get_csrf_token")
    return JsonResponse({"token": get_token(request)}) 


class EmailAPI(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        message=request.data.get('message')
        send_mail(
            'Support mail',
            message,
            request.user.email,
            [DEFAULT_TO_EMAIL1,DEFAULT_TO_EMAIL2,DEFAULT_TO_EMAIL3],
            fail_silently=False
        )
        return Response({"status":True,"message":"Mail successfully sent"})

class LoginAPI(APIView):

    permission_classes = [AllowAny]
    def get(self, request):
        users_obj = User.objects.all()
        if not users_obj.exists():
            return Response({"status": False, "message": "No user exists"}, status=status.HTTP_404_NOT_FOUND)
        serializers = UserSerializer(users_obj, many=True)
        return Response({"status": True, "data": serializers.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('rememberMe', False)

        if not email or not password:
            return Response(
                {"status": False, "message": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": False, "message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({"status": False, "message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        if remember_me:
            print("remember me is checked")
        else:
            print("remember me is not checked")

        cookie_max_age = 7 * 24 * 60 * 60 if remember_me else 24 * 60 * 60

        res = Response({
            "status": True,
            "message": "Successfully logged in",
            "access": access_token
        }, status=status.HTTP_200_OK)
        res.set_cookie(
            key='refresh',
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=cookie_max_age
        )
        return res

    def patch(self, request):
        data = request.data
        email = data.get('email')

        try:
            obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": False, "message": "No user exists"}, status=status.HTTP_404_NOT_FOUND)

        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')

        if new_password:
            if new_password != confirm_password:
                return Response({"status": False, "message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(new_password)
            obj.save()
            return Response({"status": True, "message": "Password updated successfully"})

        serializer = UserSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Successfully updated"})
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        data = request.data
        email = data.get('email')
        user = User.objects.filter(email=email)
        user.delete()
        return Response({"status": True, "message": "Successfully deleted"})

class SignupAPI(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data.copy()
        remember_me = data.pop('rememberMe', False)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        cookie_max_age = 7 * 24 * 60 * 60 if remember_me else 24 * 60 * 60

        res = Response({
            "status": True,
            "message": "Successfully signed up",
            "access": access_token
        }, status=status.HTTP_200_OK)
        res.set_cookie(
            key='refresh',
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=cookie_max_age
        )
        return res

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        res = Response({"status": True, "message": "Successfully logged out"})
        res.delete_cookie('refresh')
        return res

class UserDetailsAPI(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        auth_header = request.headers.get("Authorization")

        print("Authorization header:", auth_header)
        # user = request.user
        # return Response({
        #     'status': True,
        #     'user': {
        #         'username': user.username,
        #         'email': user.email,
        #     }
        # }, status=status.HTTP_200_OK)
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"status": False, "message": "Not logged in"}, status=401)

        try:
            refresh_token = RefreshToken(refresh)
            user = User.objects.get(id=refresh_token['user_id'])
            return Response({
                "status": True,
                "user": {
                    "username": user.username,
                    "email": user.email,
                }
            })
        except Exception:
            return Response({"status": False, "message": "Invalid refresh"}, status=401)

class RefreshTokenAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        refresh = request.COOKIES.get('refresh')
        if not refresh:
            return Response({"status": False, "message": "Refresh token expired"},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh_token = RefreshToken(refresh)
            new_access = str(refresh_token.access_token) 
            return Response({"status": True, "access": new_access})
        except TokenError:
            return Response({"status": False, "message": "Token error occurred"},
                            status=status.HTTP_401_UNAUTHORIZED)
