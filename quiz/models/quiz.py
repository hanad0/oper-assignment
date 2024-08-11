from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(
        unique=True, max_length=255, db_index=True, null=True, blank=True
    )
    passing_score_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator_quizzes"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
