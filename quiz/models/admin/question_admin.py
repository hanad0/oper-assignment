from django.contrib import admin

from quiz.models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "created_at", "created_by")
    list_filter = ("quiz", "quiz__created_by", "created_at")
    inlines = [AnswerInline]

    def created_by(self, obj):
        return obj.quiz.created_by


admin.site.register(Question, QuestionAdmin)
