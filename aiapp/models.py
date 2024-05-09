from django.db import models
from user.models import User  # Import the User model from your app

class UserInteractionCollection(models.Model):
  title = models.CharField(max_length=200)
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  #def set_title(self, generated_title):
  #  self.title=generated_title
  #  return self.save()
  
  class Meta:
    ordering = ['updated_at']

  def __str__(self):
    return self.title

class Interaction(models.Model):
  user_chat = models.TextField(blank=False, help_text='Enter the prompt text here')
  response_chat  = models.TextField(blank=False, help_text='Enter the user response here')
  image = models.ImageField(upload_to='images/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  interaction_collection = models.ForeignKey(UserInteractionCollection, on_delete=models.CASCADE)
  interaction_type = models.CharField(max_length=50, choices=[('TEXT', 'Text'), ('IMAGE', 'Image'), ('CODE', 'Code')], default='TEXT')
