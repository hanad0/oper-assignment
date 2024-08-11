from drf_spectacular.utils import extend_schema
from rest_framework import permissions, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from quiz.models import QuizProgress
from quiz.participant.serializers.quiz_progress import (
    QuizProgressSerializer,
    DetailedQuizProgressSerializer,
)
from quiz.permissions import IsQuizParticipant


@extend_schema(tags=["Quizzes for Participants"])
class QuizViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, IsQuizParticipant]
    filter_backends = [SearchFilter]
    search_fields = ["quiz__title", "quiz__slug"]

    def get_queryset(self):
        queryset = QuizProgress.objects.filter(user=self.request.user).select_related(
            "quiz"
        )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("quiz__questions__answers")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedQuizProgressSerializer
        return QuizProgressSerializer
