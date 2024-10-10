from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
UserModel = get_user_model()

class UserInputSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4)
    password1 = serializers.CharField(max_length=15, min_length=6)
    password2 = serializers.CharField(max_length=15, min_length=6)
    email = serializers.EmailField()
    first_name=serializers.CharField(max_length=50,required=False)
    last_name=serializers.CharField(max_length=50,required=False)
    def validate_username(self,value):
        if UserModel.objects.filter(username=value).first():
            raise serializers.ValidationError("Username exist")
        return value
    def validate_email(self,value):
        if UserModel.objects.filter(email=value).first():
            raise serializers.ValidationError("Email already exist")
        return value  
    def validate_password1(self, value: str):
        if len(self.data["password2"]) != len(value):
            raise serializers.ValidationError("Password length mismatch")
        if value != self.data["password2"]:
            raise serializers.ValidationError("Password mismatch")
        return value

    def create(self, validated_data):
        validated_data["password"] = validated_data["password1"]
        del validated_data["password1"]
        del validated_data["password2"]
        return UserModel.objects.create_user(**validated_data)
