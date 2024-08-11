from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from quiz.creator.filters.quiz_progress_filter import QuizProgressFilter
from quiz.creator.serializers.quiz_progress import (
    QuizProgressSerializer,
    DetailedQuizProgressSerializer,
)
from quiz.models import QuizProgress
from quiz.permissions import IsQuizCreator


@extend_schema(tags=["Quizz Progress List for Creators"])
class QuizProgressViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = QuizProgress.objects.all()
    serializer_class = QuizProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = QuizProgressFilter
    pagination_class = PageNumberPagination
    ordering_fields = [
        "submit_time",
        "score",
    ]
    ordering = ["-submit_time"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.select_related("quiz", "user").filter(
            quiz=self.kwargs["quiz_id"], quiz__created_by=user
        )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "user_answers__question", "user_answers__answer"
            )
        return queryset.select_related("quiz", "user").filter(
            quiz=self.kwargs["quiz_id"], quiz__created_by=user
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedQuizProgressSerializer
        return super().get_serializer_class()
