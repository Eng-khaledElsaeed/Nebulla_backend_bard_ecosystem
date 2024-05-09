from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import json

# serilaizer
from .serializers import UserRegisterSerializer
from .serializers import UserSerializer
from .serializers import UserLoginSerializer
#utility
from Bard_ecosystem_BE.utils.user_utility import get_all_user_fields, is_email_found
from Bard_ecosystem_BE.utils.utility import encrypt_token,is_user_authenticated


class RegisterView(APIView):
    def post(self, request):
        # Convert additional_user_info to string
        #additional_user_info = request.data.get('additional_user_info', {})
        #request.data['additional_user_info'] = json.dumps(additional_user_info)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            token = encrypt_token(user)
            user_data=get_all_user_fields(user)
            return Response(
                {'user': user_data, 'token': token},
                status=status.HTTP_201_CREATED
            )
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Extract user from validated data
            #user.additional_user_info=json.loads(user.additional_user_info)
            token = encrypt_token(user)
            user_data=get_all_user_fields(user)
            return Response({'token': token,"user":user_data}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddUserView(APIView):
    def post(self, request):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            serializer = UserRegisterSerializer(data=request.data,context={'request': request})
            if serializer.is_valid():
                # Check for existing email before saving the user
                if is_email_found(serializer.validated_data['email']):
                    return Response({'message': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = serializer.save()
                    print(f"User created successfully: {user}")
                    return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
       

class GetAllUsersView(APIView):
    def get(self, request):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            print(users)
            return Response({'message':serializer.data}, status=status.HTTP_200_OK)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
        
        
        
class GetUserView(APIView):
    def get(self, request):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            try:
                user = User.objects.get(pk=auth_result['auth_result']['id'])
                print(user)
            except User.DoesNotExist:
                return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
        
        
class UpdateUserView(APIView):
    def put(self, request,user_id):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({'message' : 'user does not exist'},status=status.HTTP_404_NOT_FOUND)
            data = json.loads(request.body.decode('utf-8'))
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'user has been updated now.','updatedUser': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])
        
        
class DeleteUserView(APIView):
    def delete(self, request,user_id):
        auth_result, is_authenticated = is_user_authenticated(request)
        if is_authenticated:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({'message' : 'user does not exist'},status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response({'message' : "User was deleted successfully."}, status=status.HTTP_200_OK)
        else:
            # Handle unauthenticated requests
            return Response({'message':auth_result['message'] }, status=auth_result['status'])