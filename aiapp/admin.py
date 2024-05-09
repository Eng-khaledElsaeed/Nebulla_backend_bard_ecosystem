from django.contrib import admin
from .models import UserInteractionCollection,Interaction
class UserInteractionGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['creator']}),
        (None,               {'fields': ['created_at']}),
        (None,               {'fields': ['updated_at']}),
    ]
    list_display = ('id','title', 'creator','created_at','updated_at')
admin.site.register(UserInteractionCollection, UserInteractionGroupAdmin)

class InteractionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['user_chat']}),
        (None,               {'fields': ['response_chat']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['created_at']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['interaction_collection']}),
        (None,               {'fields': ['interaction_type']}),
    ]
    list_display = ('id','user_chat', 'response_chat','image','created_at','updated_at','interaction_collection','interaction_type')
admin.site.register(Interaction, InteractionAdmin)

