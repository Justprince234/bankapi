from django.urls import path

from knox import views as knox_views
from .views import RegisterAPI, LoginAPIView, UserAPI, UserDataList, UserDataAuth, HistoryAPI, PendingTransferAPI

urlpatterns = [
    # path('api/request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    # path('api/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('api/password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/history/<str:email>/', HistoryAPI.as_view(), name='history'),
    path('api/pendingtransfer/<str:email>/', PendingTransferAPI.as_view(), name='pending-transfer'),
    # path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/updateuser/', UserDataList.as_view()),
    path('api/userdataauth/<str:email>/', UserDataAuth.as_view()),
]