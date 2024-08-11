from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from quiz.creator.serializers.user import UserSerializer
from quiz.permissions import IsQuizCreator


@extend_schema(tags=["Quiz Participant List"])
class QuizParticipantListView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

    def get_queryset(self):
        return User.objects.filter(groups__name="quiz_participant")
