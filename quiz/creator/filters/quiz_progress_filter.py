import django_filters
from django.contrib.auth.models import User

from quiz.models import QuizProgress


class QuizProgressFilter(django_filters.FilterSet):
    participant = django_filters.ModelChoiceFilter(
        field_name="user", queryset=User.objects.all()
    )

    class Meta:
        model = QuizProgress
        fields = ["status"]
