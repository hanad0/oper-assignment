from django.db import models
from .quiz_progress import QuizProgress
from .question import Question
from .answer import Answer


class UserAnswer(models.Model):
    user_quiz = models.ForeignKey(
        QuizProgress, on_delete=models.CASCADE, related_name="user_answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField()
