from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound

from quiz.models import Question, Quiz
from ..serializers.question import QuestionSerializer
from ...permissions import IsQuizCreator


class QuizParentMixin(viewsets.GenericViewSet):
    def get_quiz(self):
        quiz_id = self.kwargs.get("quiz_id")
        try:
            return Quiz.objects.get(id=quiz_id, created_by=self.request.user)
        except Quiz.DoesNotExist:
            raise NotFound(detail="Quiz not found")

    def get_queryset(self):
        quiz = self.get_quiz()
        return Question.objects.filter(quiz=quiz)

    def get_object(self):
        quiz = self.get_quiz()
        pk = self.kwargs.get("pk")
        try:
            return Question.objects.get(quiz=quiz, pk=pk)
        except Question.DoesNotExist:
            raise NotFound(detail="Not found")

    def perform_create(self, serializer):
        quiz = self.get_quiz()
        serializer.save(quiz=quiz)


@extend_schema(tags=["Creator Question"])
class QuestionViewSet(QuizParentMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]
