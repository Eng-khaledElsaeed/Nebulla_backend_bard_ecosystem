from rest_framework import serializers
from .models import UserInteractionCollection, Interaction


class UserInteractionCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteractionCollection
        fields = ('id', 'title', 'creator','created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')  # Mark created/updated fields as read-only
    

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ('id', 'user_chat', 'response_chat','image','created_at','updated_at', 'interaction_collection', 'interaction_type')
        read_only_fields = ('created_at','updated_at','interaction_collection','image')  # Mark timestamp and collection as read-only
