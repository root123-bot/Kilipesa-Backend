from django.shortcuts import render
from django.contrib.auth import get_user_model
# , ResetPasswordEmailRequestSerializer
from MkulimaBackend.register.serializers import RegistrationSerializer, EmailSerializer, ResetPasswordSerializer
from MkulimaBackend.mkulima.models import Profile
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from MkulimaBackend.mkulima.models import *
from rest_framework import status

class PasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))

            token = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse(
                "password_reset_confirm", kwargs={'uidb64': encoded_pk, 'token': token}
            )

            # If we have the domain name we can use it here instead of http://localhost:8000
            reset_url = f"https://84fd-41-59-195-10.ngrok-free.app{reset_url}"

            # then you should send this url to the user via email
            send_mail(
                "Password Reset",
                f'Hi {user.email}, Please use this link to reset your password {reset_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            return Response({
                "detail": "Password reset link has been sent to your email"
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "detail": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        

password_reset = PasswordReset.as_view()


class CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        password = request.data['password']
        user_group = request.data.get('user_group', None)
        
        
        try:
            if password:
                password_hash = make_password(password)

                user = get_user_model().objects.create(
                    email=request.data['email'], password=password_hash)
                user.save()
                if (user_group == "Gatherman"):
                    gatherman = GatherProfile.objects.create(
                        user=user,
                        user_group=user_group,
                    )
                    gatherman.save()
                    
                    serializer = RegistrationSerializer(user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            # , status=status.HTTP_400_BAD_REQUEST
            return Response({"err": 'Sorry password field should not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({'err': str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data['id']
        password = request.data.get('password', None)
        oldPassword = request.data.get('old', None)

        user = get_user_model().objects.get(id=user_id)

        if password and oldPassword:
            print('Im inside to check this...')
            print(oldPassword, password)
            # check password return true if password exist and not otherwise... https://stackoverflow.com/questions/16700968/check-existing-password-and-reset-password
            if user.check_password(oldPassword):
                print('I verified it to true')
                password_hash = make_password(password)
                user.password = password_hash
                user.save()

                # seriailize = RegistrationSerializer(user)
                return Response({"message": "Everything is good, password has been changed.."})

        return Response({"error": "Sorry password field should not be empty"})


class PasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))

            token = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse(
                "reset-password", kwargs={'encoded_pk': encoded_pk, 'token': token}
            )

            reset_url = f"localhost:8000{reset_url}"

            send_mail(
                'Reset Password',
                f'Click this link to reset your password http://localhost:3000/resetConfirm?api={reset_url}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            return Response({
                'message': 'Everything is good see your email for link to reset your password ' + reset_url
            },
                status=status.HTTP_200_OK
            )

        else:
            Response({
                'message': 'User does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'kwargs': kwargs}
        )

        serializer.is_valid(raise_exception=True)

        return Response({"message": 'Password reset complete'}, status=status.HTTP_200_OK)


change_password = ChangePasswordAPIView.as_view()
create_user_api = CreateUserAPIView.as_view()
