from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import (UserCreateView, UserVerifyView, UserChangePasswordView,
                            UserDeleteView, UserView, ProfileView)

app_name = 'accounts'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/verify/', UserVerifyView.as_view(), name="user_verify"),
    path('user/create/', UserCreateView.as_view(), name="user_create"),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name="user_delete"),
    path('user/change-password/', UserChangePasswordView.as_view(), name="user_change_password"),
    path('user/<int:pk>/', UserView.as_view(), name="user"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),

]
