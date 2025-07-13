from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import *
from rest_framework import  status
from rest_framework.response import  Response
from rest_framework.permissions import AllowAny
from random import randint
from django.template.loader import render_to_string
from django.core.cache import cache
from .tasks import *
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
from uuid import uuid4
# Create your views here.

class RegisterAPIView(APIView):
    permission_classes =[AllowAny]
    def post(self,request):

        try:
            data = request.data
            serializer = RegisterSerializer(data = data)
        except Exception as e:
            raise f"Please Enter Valid Data {e}"

        if not serializer.is_valid():
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        otp = randint(100000,999999)

        token = AccessToken()
        token.set_exp(lifetime= timedelta(minutes=10))

        subject = "Email Verification"
        html_content = render_to_string('email/send_verification_email.html', {'name': validated_data['username'], 'otp': otp})
        text_content = f"Hello! {validated_data['username']}.\n Here is your otp :{otp}. \n It is valid for 10 minutes"
        send_mail.delay(subject,html_content,text_content, validated_data['email'])

        key = uuid4()
        token['key'] = str(key)

        cache.set(f'{str(key)}',{
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'password2': validated_data['password2'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'dob': validated_data['dob'],
            'gender': validated_data['gender'],
            'phone_number': str(validated_data['phone_number']),
            'otp': str(otp)
        },timeout=600)


        return Response({"message":"Please verify your email","otp":str(otp),"key":str(key)},status=status.HTTP_200_OK)

class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        key = request.data.get('key')
        input_otp = request.data.get('otp')
        data = cache.get(key)

        if str(input_otp) != str(data['otp']) :
            return Response({'error': 'Please enter correct otp'}, status= status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({"message": "Account created successful"}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes= [AllowAny]
