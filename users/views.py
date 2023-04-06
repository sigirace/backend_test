import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from . import serializers
from . models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        # json -> django
        serializer = serializers.PrivateUserSerializer(user,
                                                       data=request.data,
                                                       partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            # django -> json
            serializer = serializers.PrivateUserSerializer(updated_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    
    def post(self, request):
        
        password = request.data.get("password")
        if not password:
            raise ParseError("password가 유효하지 않습니다.")
        
        serializer = serializers.PrivateUserSerializer(data=request.data) # json -> django

        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    # urls: @<str:username>
    def get(self, request, username):
        try:
            user = User.objects.get(username = username)
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    # urls: change-password
    def put(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        user = request.user

        if not old_password or not new_password:
            raise ParseError("password가 유효하지 않습니다.")

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print("kang")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class LogIn(APIView):
    
    def post(self, request):
        un = request.data.get("username")
        pw = request.data.get("password")

        if not un or not pw:
            raise ParseError("유효하지 않은 입력입니다.")
        
        user = authenticate(request=request,
                            username=un,
                            password=pw,)
        
        if user:
            login(request, user)
            return Response({"ok":"hi"})
        else:
            return Response({"error": "id 혹은 pw를 확인하세요."})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
    

class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
            # https://velog.io/@pjh1011409/%EB%A1%9C%EA%B7%B8%EC%9D%B8
        else:
            return Response({"error": "wrong password"})