from django.urls import path
from .views import UserlistColectionsView,UserlistInteractionsView
from .views import StartInteractionView,StartInteractionWithCollectionIdView,generatetitle
from .views import ImageUploadView

urlpatterns=[
#--------- get -----------
	path('getUserlistColections/', UserlistColectionsView.as_view(), name='UserlistColections'),
	path('getUserlistInteractions/<int:collection_id>/', UserlistInteractionsView.as_view(), name='UserlistInteractions'),
 

#--------- post -------------
	path('StartInteractionView/', StartInteractionView.as_view(), name='StartInteractionView'),
	path('StartInteractionView/<int:collection_id>/', StartInteractionWithCollectionIdView.as_view(), name='StartInteractionWithCollectionIdView'),
 

    path('generatetitle/', generatetitle.as_view(), name='generatetitle'),
    path('upload-image/', ImageUploadView.as_view(), name='upload_image')
    
    
    #path('getAllInteractions/', views.get__all_users_interaction, name='get__all_users_interaction'),
    #path('getInteraction/<int:iteraction_id>/', views.get_specific_user_interactions, name='get_specific_user_interactions'),
    #path('update_user_interaction/<int:iteraction_id>/', views.update_user_interaction, name='update_user_interaction'),
    ##path('deleteInteraction/<int:iteraction_id>/', views.delete_Prompt_by_id, name='delete_Prompt_by_id'),
]