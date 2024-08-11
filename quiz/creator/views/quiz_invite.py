from django.contrib.auth.models import User
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.const.user_groups import QUIZ_PARTICIPANT
from quiz.models import Quiz
from quiz.models.quiz_progress import QuizProgress
from quiz.permissions import IsQuizCreator
from quiz.util.email_service import EmailService, InvitationContext


@extend_schema(tags=["Creator Quiz Invite"])
class QuizInviteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsQuizCreator]

    @transaction.atomic
    def post(self, request, quiz_id, user_id):
        quiz = get_object_or_404(
            Quiz.objects.filter(created_by=request.user), id=quiz_id
        )
        user = get_object_or_404(
            User.objects.filter(groups__name=QUIZ_PARTICIPANT), id=user_id
        )

        quiz_progress, created = QuizProgress.objects.get_or_create(
            user=user, quiz=quiz
        )
        host = request.get_host()
        context = InvitationContext(
            sender=request.user, quiz_progress=quiz_progress, host=host, receiver=user
        )
        EmailService.send_invitation_email(context)

        return Response(
            {
                "message": "User invited successfully.",
                "quiz_progress_id": quiz_progress.id,
                "created": created,
            },
            status=status.HTTP_200_OK,
        )
