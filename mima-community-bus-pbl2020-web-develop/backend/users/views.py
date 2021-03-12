from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import update_last_login

from .serializers import (
    LoginTokenSerializer, UserSerializer
)
from .models import Users


class LoginTokenObtaionView(TokenObtainPairView):
    """
    # トークンの取得
    ## Response Example
    ```
    {
      "access_token": "{token}",
      "token_type": "bearer",
      "expire_in": 60
    }
    ```
    """
    serializer_class = LoginTokenSerializer
    def post(self, request, *args, **kwargs):
        result = super().post(request)
        if result.status_code == 200:
            user = Users.objects.get(email=request.data['email'])
            update_last_login(None, user)
        return result


class UserView(APIView):
    def get(self, request):
        """
        # ユーザー情報管理API
        ## Response 200 Example
        ```
        {
            "users": [
                {
                    "id": "1",
                    "name": "test",
                    "email": "test@example.com"
                },
                {...}
            ]
        }
        ```
        """
        users = Users.objects.all()
        resp_data = {}
        resp_data['users'] = [
            {
                "id": f'{user.id}',
                "name": user.username,
                "email": user.email
            }
            for user in users
        ]
        return Response(resp_data)

    def post(self, request):
        """
        # ユーザー登録API
        ## Response 200 Example
        {
            "result": true,
            "name": "ehimeict",
            "phone_number": "08038473847",
            "email": "ehimeict@gmail.com",
            "message": "User creation succeeded."
        }
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.save()
            data['result'] = True
            data['message'] = "ユーザーの登録に成功しました。"
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    """
    # アカウント情報の取得
    ## Response Example
    ```
    {
      "id": "1",
      "name": "ehimeict",
      "phone_number": "08038473847",
      "email": "ehimeict@gmail.com"
    }
    ```
    """
    def get(self, request):
        user = request.user
        resp_data = {
            'id': f'{user.id}',
            'name': user.username,
            'phone_number': user.phone_number,
            'email': user.email
        }
        return Response(resp_data)
