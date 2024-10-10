from rest_framework import serializers
from django.contrib.auth import get_user_model
from userAuth.models import ResetToken
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
            raise serializers.ValidationError("Username already exist")
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

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        exclude=['password','groups','user_permissions']

class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4,required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=15, min_length=6)
    
    def validate(self,data):
        # Global validation
        if not any(data.values()):
            raise serializers.ValidationError("At least one of username, email, or password must be provided.")
        
        # Check if email or username exists
        if not data.get("email") and not data.get("username"):
            raise serializers.ValidationError("Either Email or Username should exist")
        
        return data


class ResetPasswordSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4,required=False)
    email = serializers.EmailField(required=False)
    password1 = serializers.CharField(max_length=15, min_length=6)
    password2 = serializers.CharField(max_length=15, min_length=6)
    
    def validate(self,data):
        # Check if email or username exists
        if not data.get("email") and not data.get("username"):
            raise serializers.ValidationError("Either Email or Username should exist")
        if len(data["password2"]) != len(data["password1"]):
            raise serializers.ValidationError("Password length mismatch")
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Password mismatch")
        return data
    
    def validate_username(self,value):
        if not UserModel.objects.filter(username=value).first():
            raise serializers.ValidationError("user doesnt exist")
        return value
    def validate_email(self,value):
        if UserModel.objects.filter(email=value).first():
            raise serializers.ValidationError("user doesnt exist")
        return value
    def update(self, validated_data):
        user=False
        username=validated_data.get("username")
        email=validated_data.get("email")
        if username:
            user=UserModel.objects.filter(username=username).first()
        if email:
            user=UserModel.objects.filter(username=username).first()
        resetToken=ResetToken.objects.get(user=user)
        if resetToken.is_expired:
            user.set_password(validated_data['password1'])
            return user
        return False