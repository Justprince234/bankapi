from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, UpdateUserSerializer, LoginSerializer, ChangePasswordSerializer, HistorySerializer, PendingTransferSerializer
from rest_framework.permissions import IsAuthenticated
from .models import UpdateUser, User, History, PendingTransfer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Change Password
from .models import User
from .serializers import ChangePasswordSerializer
# Create your views here.

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])

        # token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        # relativeLink = reverse('verify-email')
        
        # absurl = 'http//'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hello'+user.first_name,'Use link below to verify your email; \n'+ absurl
        # data = {'email_body':email_body, 'email_subject':'Verify your email', 'to_email':user.email,}

        # Util.send_email(data)


        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

# @swagger_auto_schema(manual_parameters=[token_param_config])
# class VerifyEmail(views.APIView):
#     serializer_class = EmailVerificationSerializer
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as identifier :
#             return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)

#         except jwt.exceptions.DecodeError as identifier :
#             return Response({'error': 'Invalid token request a new one'}, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
        
# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Get History API
class HistoryAPI(LoginRequiredMixin, generics.ListAPIView):
    Model = History
    serializer_class = HistorySerializer

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        queryset = History.objects.filter(user_id=user)
        return queryset.order_by('-transaction_date')


# Get PendingTransfer API
class PendingTransferAPI(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = PendingTransferSerializer

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        queryset = PendingTransfer.objects.filter(user_id=user)
        return queryset.order_by('-transfer_date')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDataList(generics.ListCreateAPIView):
    queryset = UpdateUser.objects.all()
    serializer_class = UpdateUserSerializer

class UserDataAuth(LoginRequiredMixin, generics.ListAPIView):
    queryset = UpdateUser.objects.all()
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        queryset = UpdateUser.objects.filter(user_id=user)
        return queryset.order_by('-date_updated')

# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = RequestPasswordResetEmailSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data['email']

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(user.id)
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(request=request).domain
#             relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            
#             absurl = 'http//'+current_site + relativeLink
#             email_body ='Hello \n Use link below to reset your password; \n'+ absurl
#             data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your Password'}

#             Util.send_email(data)

#         return Response({'success': 'Please check your email, a reset password link has been sent.'}, status=status.HTTP_200_OK)

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self, request, uidb64, token):
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

#             return Response({'success':True, 'message': 'Credentials valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

#         except DjangoUnicodeDecodeError:
#             if not PasswordResetTokenGenerator():
#                 return Response({'error': 'Inavalid token, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         serialzer = self.serializer_class(data=request.data)

#         serialzer.is_valid(raise_exception=True)

#         return Response({'success':True, 'message':'Password reset successful'}, status=status.HTTP_200_OK)