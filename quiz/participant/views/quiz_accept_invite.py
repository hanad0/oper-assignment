from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ...const.quiz_status import QUIZ_ACCEPTED, QUIZ_PASSED, QUIZ_FAILED
from ...models import QuizProgress
from ...permissions import IsQuizParticipant


@extend_schema(tags=["Quiz Participant Accept Invite"])
class AcceptQuizInviteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsQuizParticipant]

    def post(self, request, quiz_progress_id):
        quiz_progress = get_object_or_404(QuizProgress, id=quiz_progress_id)
        if quiz_progress.status == QUIZ_ACCEPTED:
            return Response(
                {"error": "Invitation already accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quiz_progress.status in (QUIZ_PASSED, QUIZ_FAILED):
            return Response(
                {"error": "Quiz already taken."}, status=status.HTTP_400_BAD_REQUEST
            )

        quiz_progress.status = QUIZ_ACCEPTED
        quiz_progress.save()

        return Response({"status": "Invitation accepted."}, status=status.HTTP_200_OK)
