from django.contrib import admin

from quiz.models import Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "is_correct",
        "question_text",
        "quiz_title",
        "created_at",
        "created_by",
    )
    list_filter = (
        "question",
        "question__quiz",
        "question__quiz__created_by",
        "created_at",
    )

    def question_text(self, obj):
        return obj.question.text

    def quiz_title(self, obj):
        return obj.question.quiz.title

    def created_by(self, obj):
        return obj.question.quiz.created_by

    question_text.short_description = "Question"
    quiz_title.short_description = "Quiz"


admin.site.register(Answer, AnswerAdmin)
