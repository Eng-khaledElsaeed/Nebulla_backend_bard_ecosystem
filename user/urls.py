from django.urls import path
from .views import RegisterView, LoginView,AddUserView,GetAllUsersView,GetUserView,UpdateUserView,DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('getUser/', GetUserView.as_view(), name='get_user_by_id'),
    path('addUser/', AddUserView.as_view(), name='create_a_new_user'),
    path('getAllUsers/', GetAllUsersView.as_view(), name='get_all_users'),
    path('updateUser/<int:user_id>/', UpdateUserView.as_view(), name='update_user_by_id'),
    path('deleteUser/<int:user_id>/', DeleteUserView.as_view(), name='delete_user_by_id'),
]
