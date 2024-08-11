from django.contrib import admin

from quiz.models import Quiz, Question, Answer
import nested_admin


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 1


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ("title", "slug", "created_by")
    search_fields = ("title", "description", "slug")
    list_filter = ("created_by", "created_at")
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
