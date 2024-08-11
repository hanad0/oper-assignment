import django_filters

from quiz.models import Quiz


class QuizFilter(django_filters.FilterSet):
    min_score = django_filters.NumberFilter(
        field_name="passing_score_percentage", lookup_expr="gte"
    )
    max_score = django_filters.NumberFilter(
        field_name="passing_score_percentage", lookup_expr="lte"
    )

    class Meta:
        model = Quiz
        fields = ["min_score", "max_score", "slug"]
