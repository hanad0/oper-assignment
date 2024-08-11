from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from .quiz import Quiz
from ..const.quiz_status import QUIZ_INVITED, QUIZ_ACCEPTED, QUIZ_PASSED, QUIZ_FAILED


class QuizProgress(models.Model):
    STATUS_CHOICES = [
        (QUIZ_INVITED, "Invited"),
        (QUIZ_ACCEPTED, "Accepted"),
        (QUIZ_PASSED, "Passed"),
        (QUIZ_FAILED, "Failed"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="participant_quizzes"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=QUIZ_INVITED
    )

    class Meta:
        verbose_name = "Quiz Progress"
        verbose_name_plural = "Quiz Progresses"
