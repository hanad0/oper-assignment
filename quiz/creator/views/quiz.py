from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from quiz.models import Quiz
from ..filters.quiz_filter import QuizFilter
from ..serializers import QuizSerializer
from ..serializers.quiz import QuizDetailSerializer
from ...permissions import IsQuizCreator


@extend_schema(tags=["Creator Quiz"])
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = QuizFilter
    pagination_class = PageNumberPagination
    ordering_fields = [
        "created_at",
        "updated_at",
        "max_attempts",
        "passing_score_percentage",
    ]
    ordering = ["-created_at"]
    search_fields = ["title", "slug", "description"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("questions", "questions__answers")
        if not user.is_staff:
            queryset = queryset.filter(created_by=user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = QuizDetailSerializer(instance)
        return Response(serializer.data)
