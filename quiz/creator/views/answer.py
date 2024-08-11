from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound

from quiz.models import Question, Answer
from ..serializers.answer import AnswerSerializer
from ...permissions import IsQuizCreator


class QuestionParentMixin(viewsets.GenericViewSet):
    def get_question(self):
        question_id = self.kwargs.get("question_id")
        try:
            return Question.objects.get(
                id=question_id, quiz__created_by=self.request.user
            )
        except Question.DoesNotExist:
            raise NotFound(detail="Question not found")

    def get_queryset(self):
        question = self.get_question()
        return Answer.objects.filter(question=question)

    def get_object(self):
        question = self.get_question()
        pk = self.kwargs.get("pk")
        try:
            return Answer.objects.get(question=question, pk=pk)
        except Answer.DoesNotExist:
            raise NotFound(detail="Not found")

    def perform_create(self, serializer):
        question = self.get_question()
        serializer.save(question=question)


@extend_schema(tags=["Creator Answer"])
class AnswerViewSet(QuestionParentMixin, viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]
