from decimal import Decimal

from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

from quiz.const.quiz_status import QUIZ_PASSED
from quiz.models import Quiz, Question, Answer, QuizProgress, UserAnswer


class Command(BaseCommand):
    help = "Load initial data into the database"

    def handle(self, *args, **kwargs):
        participant = User.objects.create_user(
            username="participant", email="participant@test.com", password="Oper1234"
        )
        creator = User.objects.create_user(
            username="creator", email="creator@test.com", password="Oper1234"
        )

        participant_group = Group.objects.get(name="quiz_participant")
        creator_group = Group.objects.get(name="quiz_creator")

        participant.groups.add(participant_group)
        creator.groups.add(creator_group)

        quiz1 = Quiz.objects.create(
            title="Quiz 1", slug="quiz1", description="Quiz 1", created_by=creator
        )
        quiz2 = Quiz.objects.create(
            title="Quiz 2", slug="quiz2", description="Quiz 2", created_by=creator
        )

        question1 = Question.objects.create(quiz=quiz1, text="Quiz 1 - Question 1")
        question2 = Question.objects.create(quiz=quiz1, text="Quiz 1 - Question 2")
        question3 = Question.objects.create(quiz=quiz1, text="Quiz 1 - Question 3")

        question4 = Question.objects.create(quiz=quiz2, text="Quiz 2 - Question 1")
        question5 = Question.objects.create(quiz=quiz2, text="Quiz 2 - Question 2")
        question6 = Question.objects.create(quiz=quiz2, text="Quiz 2 - Question 3")

        answer1 = Answer.objects.create(
            question=question1, text="Answer 1", is_correct=True
        )
        Answer.objects.create(question=question1, text="Answer 2", is_correct=False)

        answer2 = Answer.objects.create(
            question=question2, text="Answer 1", is_correct=True
        )
        Answer.objects.create(question=question2, text="Answer 2", is_correct=False)

        answer3 = Answer.objects.create(
            question=question3, text="Answer 1", is_correct=True
        )
        Answer.objects.create(question=question3, text="Answer 2", is_correct=False)

        Answer.objects.create(question=question4, text="Answer 1", is_correct=True)
        Answer.objects.create(question=question4, text="Answer 2", is_correct=False)

        Answer.objects.create(question=question5, text="Answer 1", is_correct=True)
        Answer.objects.create(question=question5, text="Answer 2", is_correct=False)

        Answer.objects.create(question=question6, text="Answer 1", is_correct=True)
        Answer.objects.create(question=question6, text="Answer 2", is_correct=False)

        quiz_progress = QuizProgress.objects.create(
            user=participant, quiz=quiz1, status=QUIZ_PASSED, score=Decimal("100.00")
        )
        UserAnswer.objects.create(
            user_quiz=quiz_progress, answer=answer1, question=question1, is_correct=True
        )
        UserAnswer.objects.create(
            user_quiz=quiz_progress, answer=answer2, question=question2, is_correct=True
        )
        UserAnswer.objects.create(
            user_quiz=quiz_progress, answer=answer3, question=question3, is_correct=True
        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded initial data"))
