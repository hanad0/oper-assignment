from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizInviteView
from .views.answer import AnswerViewSet
from .views.question import QuestionViewSet
from .views.quiz_participant import QuizParticipantListView
from .views.quiz_progress import QuizProgressViewSet

router = DefaultRouter()
router.register(r"quizzes", QuizViewSet, basename="creator-quiz")
router.register(
    r"quizzes/(?P<quiz_id>\d+)/progress", QuizProgressViewSet, basename="quiz-progress"
)
router.register(
    r"quizzes/(?P<quiz_id>\d+)/questions", QuestionViewSet, basename="question"
)
router.register(
    r"quizzes/questions/(?P<question_id>\d+)/answers", AnswerViewSet, basename="answer"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "quizzes/<int:quiz_id>/invite/<int:user_id>/",
        QuizInviteView.as_view(),
        name="invite",
    ),
    path("participants", QuizParticipantListView.as_view(), name="participants"),
]
