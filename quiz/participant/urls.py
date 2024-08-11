from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quiz.participant.views.quiz_accept_invite import AcceptQuizInviteView
from quiz.participant.views.quiz_list import QuizViewSet
from quiz.participant.views.quiz_submit import QuizSubmitView

router = DefaultRouter()
router.register(r"quizzes", QuizViewSet, basename="participant-quiz")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "quizzes/accept/<int:quiz_progress_id>/",
        AcceptQuizInviteView.as_view(),
        name="accept-invite",
    ),
    path(
        "quizzes/submit/<int:quiz_progress_id>/",
        QuizSubmitView.as_view(),
        name="submit-quiz",
    ),
]
