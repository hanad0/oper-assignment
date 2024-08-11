from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["username", "password"],
            }
        },
        responses={
            status.HTTP_200_OK: {"description": "Login successful"},
            status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
        },
        description="Login endpoint to authenticate users and create a session.",
        summary="User Login",
        tags=["Login"],
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
