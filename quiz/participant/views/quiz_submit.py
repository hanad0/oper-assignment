from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.const.quiz_status import QUIZ_INVITED, QUIZ_PASSED, QUIZ_FAILED
from quiz.models import QuizProgress, UserAnswer
from quiz.participant.serializers.quiz_submission import QuizSubmissionSerializer
from quiz.permissions import IsQuizParticipant
from quiz.util.quiz_score_service import (
    QuizScoreService,
    QuizScoreContext,
    AnswerSubmission,
    QuizScoreResult,
)


@extend_schema(tags=["Quiz Participant Submit"])
class QuizSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsQuizParticipant]
    serializer_class = QuizSubmissionSerializer

    @transaction.atomic
    def post(self, request, quiz_progress_id):
        quiz_progress = get_object_or_404(
            QuizProgress.objects.select_related("quiz").prefetch_related(
                "quiz__questions", "quiz__questions__answers"
            ),
            id=quiz_progress_id,
        )
        if quiz_progress.status == QUIZ_INVITED:
            return Response(
                {"error": "Invitation not accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quiz_progress.status in (QUIZ_PASSED, QUIZ_FAILED):
            return Response(
                {"error": "Quiz already taken."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers_data = serializer.validated_data.get("answers", [])
        answers = [AnswerSubmission(**answer) for answer in answers_data]

        quiz_score_context = QuizScoreContext(
            quiz_submission=answers, quiz_progress=quiz_progress
        )

        quiz_score_result: QuizScoreResult = QuizScoreService.get_score_and_status(
            quiz_score_context
        )

        quiz_progress.score = quiz_score_result.result
        quiz_progress.status = quiz_score_result.quiz_status.value
        quiz_progress.submit_time = timezone.now()
        quiz_progress.save()

        UserAnswer.objects.bulk_create(quiz_score_result.answers)

        return Response({"status": quiz_progress.status}, status=status.HTTP_200_OK)
