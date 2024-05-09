import json
from user.models import User

from rest_framework import status
from rest_framework.response import Response


def get_all_user_fields(user):
    """
    Returns a dictionary containing all user fields of a User object, excluding the password,username.

    Args:
        user: A User object.

    Returns:
        A dictionary containing all user fields except password.
    """

    user_data = {
        'user_id':user.id,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'additional_user_info': user.additional_user_info,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined.isoformat(),  # Convert datetime to ISO format
        'updated_at': user.updated_at.isoformat(),
    }
    # Add any other fields you want to include from the User model

    return user_data


def is_email_found(requestEmail):
    # Query the User model to check if the email already exists
    return User.objects.filter(email=requestEmail).exists()
