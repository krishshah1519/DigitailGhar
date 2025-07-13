from rest_framework.serializers import *
from .models import *

class RegisterSerializer(ModelSerializer):
    password2 = CharField(write_only= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'dob', 'gender', 'phone_number']
        extra_kwargs ={
            "password": {"write_only": True},
        }
    def validate(self,data):
        if data['password'] != data['password2']:
            raise ValidationError("The passwords do not match")
        if User.objects.filter(username = data['username']).exists():
            raise ValidationError("THe username already exists")
        if User.objects.filter(email = data['email']).exists():
            raise ValidationError("The email already exists")
        return data

    def create(self,validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password= password, **validated_data)
        return user