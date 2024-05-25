from django.db import models
import secrets
import json
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    additional_user_info = models.TextField(blank=True)  # optional field for any extra info about the user
    is_active = models.BooleanField(default=True)         
    is_staff = models.BooleanField(default=False)          
    is_superuser = models.BooleanField(default=False)          
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, raw_password):
        salt = secrets.token_urlsafe(32)  # Generate a random salt
        hashed_password = make_password(raw_password, salt=salt)
        self.password = hashed_password
        
    def set_additional_user_info(self, additional_data):
        self.additional_user_info = json.dumps(additional_data)
        
    def retrive_additional_user_info(self, additional_data):
        return json.loads(additional_data)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class UserLevelState(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    level_1 = models.BooleanField(default=False)         
    level_2 = models.BooleanField(default=False)          
    level_3 = models.BooleanField(default=False)          
    
    def changeLevelStateActive(self,level_num):
        # Check if the level_num attribute exists
        level_attr = f"level_{level_num}"
        if hasattr(self, level_attr):
            setattr(self, level_attr, True)
            self.save()