
from rest_framework import serializers
from .models import User  # Replace with your custom user model path if applicable
import json


class TokenDataSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    

class AdditionalUserInfoField(serializers.Field):
    
    def to_representation(self, value):
        return json.dumps(value)

    def to_internal_value(self, data):
        return json.dumps(data)


class UserSerializer(serializers.ModelSerializer):
    additional_user_info = AdditionalUserInfoField()
    class Meta:
        model = User
        fields = '__all__'

    
class UserRegisterSerializer(serializers.ModelSerializer):
    additional_user_info = AdditionalUserInfoField(required=False)
    confirmation_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields ='__all__'
        extra_kwargs = {
            'confirmation_password': {"write_only": True, "required": True,"allow_null": False}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        confirmation_password = attrs.get('confirmation_password')
        
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise serializers.ValidationError(detail=detail)
        
        if password != confirmation_password:
            raise serializers.ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"message": "Email already taken!"})
        return attrs
    
    def create(self, validated_data):
        # Pop the confirmation_password before creating the user
        confirmation_password = validated_data.pop('confirmation_password', None)
        user = User.objects.create(**validated_data)
        print("User created",user)
        user.set_password(user.password)  # Set and hash the password
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
                
        user = User.objects.filter(username=username).first()  # Filter by username
        print(user)
        
        if not user:
            raise serializers.ValidationError('User does not exist!')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials!')
        
        user.additional_user_info=json.loads(user.additional_user_info)
        attrs['user'] = user
        return attrs