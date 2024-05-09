from cryptography.fernet import Fernet
import json
import base64
import os  # For secure random number generation
from django.conf import settings
from user.models import User
from rest_framework import status
from rest_framework.response import Response
def generate_encryption_key():
    """Generates a random, base64-encoded key (32 bytes)."""
    key = base64.urlsafe_b64encode(os.urandom(32))
    return key


ENCRYPTION_KEY = settings.ENCRYPTION_KEY
print(ENCRYPTION_KEY)

def encrypt_token(user):
    """Encrypts user data using the stored encryption key."""
    user_data={'user_id':user.id, 'username':user.username,'email':user.email}
    fernet = Fernet(ENCRYPTION_KEY)
    user_data_json = json.dumps(user_data)  # Serialize data to JSON
    user_data_bytes = user_data_json.encode()  # Encode JSON string to bytes
    encrypted_data = fernet.encrypt(user_data_bytes)
    return encrypted_data.decode()  # Convert back to a string for easier handling


def decrypt_token(encrypted_data):
    """Decrypts encrypted data using the stored encryption key."""
    fernet = Fernet(ENCRYPTION_KEY)
    user_data_json = json.dumps(encrypted_data)  # Serialize data to JSON
    user_data_bytes = user_data_json.encode()  # Encode JSON string to bytes
    decrypted_data = fernet.decrypt(user_data_bytes)
    return decrypted_data.decode()  # Convert back to a string


def is_user_authenticated(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Missing authorization header', 'status': status.HTTP_401_UNAUTHORIZED}, False

        # Extract the token from the Authorization header
        _, token = auth_header.split()
        print("Authentication token :", token)

        # Decrypt and parse the token
        user_token_data = json.loads(decrypt_token(token))
        if user_token_data:
            # Check if the user exists based on the token data
            is_user_exist = User.objects.filter(username=user_token_data['username'], id=user_token_data['user_id']).exists()
            if is_user_exist:
                return {'message': 'Authorization successful', 'status': status.HTTP_200_OK, "user_token_data": user_token_data}, True,
            else:
                return {'message': 'Authorization failed', 'status': status.HTTP_401_UNAUTHORIZED, "user_token_data": user_token_data}, False
        else:
            return {'message': 'Invalid token', 'status': status.HTTP_401_UNAUTHORIZED, "user_token_data": user_token_data}, False
    except Exception as e:
        print("Error:", e)
        return {'message': 'Token extraction error, please login again', 'status': status.HTTP_401_UNAUTHORIZED}, False