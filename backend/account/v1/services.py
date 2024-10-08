from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404

User = get_user_model()


class AccountServices:
    def create_user(self, email: str, password: str):
        from account.v1.serializers import UserResponseSerializer

        user = User.objects.create_user(email=email, password=password)
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        data = {
                "id": user.id,
                "email": user.email,
                "access_token": str(refresh),
                "refresh": str(access_token)
                }

        return data


    def login(self, email: str, password: str):
        from account.v1.serializers import UserResponseSerializer

        user: User = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid Credentials")

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        data = {
                "id": str(user.id),
                "email": user.email,
                "refresh": str(refresh),
                "access_token": str(access_token),
            }


        return data


account_service = AccountServices()
