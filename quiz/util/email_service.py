from django.contrib.auth.models import User
from django.core.mail import send_mail


from dataclasses import dataclass

from quiz.models import QuizProgress


@dataclass
class InvitationContext:
    receiver: User
    sender: User
    quiz_progress: QuizProgress
    host: str


class EmailService:

    @staticmethod
    def send_invitation_email(context: InvitationContext):
        subject = f"You're invited to participate in the quiz: {context.quiz_progress.quiz.title}"
        message = (
            f"Hello {context.receiver.username},\n\nYou have been invited to take the quiz titled '{context.quiz_progress.quiz.title}'. "
            f"There is no client yet, so after you login with your username, please send a POST request to:\n\nhttp://{context.host}/api/participant/quizzes/accept/{context.quiz_progress.id}/\n\nGood luck!"
        )
        from_email = context.sender.email
        recipient_list = [context.receiver.email]

        send_mail(subject, message, from_email, recipient_list)
