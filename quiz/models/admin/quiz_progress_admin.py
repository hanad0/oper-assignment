from django.contrib import admin

from quiz.models import QuizProgress, UserAnswer


class UserAnswerInline(admin.StackedInline):
    model = UserAnswer
    extra = 1


class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ("quiz", "user", "score", "status")
    list_filter = ("quiz", "user")
    inlines = [UserAnswerInline]


admin.site.register(QuizProgress, QuizProgressAdmin)
