from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User, Group

from quiz.const.quiz_status import QUIZ_PASSED, QUIZ_INVITED, QUIZ_ACCEPTED
from quiz.models import Quiz, Question, Answer, QuizProgress


class QuizSubmitViewTests(APITestCase):

    def setUp(self):
        # Set up a user and group
        self.user = User.objects.create_user(
            username="participant", password="password"
        )
        group = Group.objects.get(name="quiz_participant")
        self.user.groups.add(group)

        # Create a quiz and questions/answers
        self.quiz = Quiz.objects.create(
            title="Sample Quiz", description="Sample Description", created_by=self.user
        )
        self.question1 = Question.objects.create(quiz=self.quiz, text="Question 1?")
        self.answer1_1 = Answer.objects.create(
            question=self.question1, text="Answer 1.1", is_correct=True
        )
        self.answer1_2 = Answer.objects.create(
            question=self.question1, text="Answer 1.2", is_correct=False
        )

        self.quiz_progress = QuizProgress.objects.create(
            user=self.user, quiz=self.quiz, status=QUIZ_INVITED
        )

        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_successful_quiz_submission(self):
        # Accept the invitation
        self.quiz_progress.status = QUIZ_ACCEPTED
        self.quiz_progress.save()

        url = reverse("submit-quiz", kwargs={"quiz_progress_id": self.quiz_progress.id})
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_id": self.answer1_1.id}
            ]
        }

        response = self.client.post(url, data, format="json")
        self.quiz_progress.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.quiz_progress.status, QUIZ_PASSED)

    def test_quiz_submission_without_accepting_invitation(self):
        url = reverse("submit-quiz", kwargs={"quiz_progress_id": self.quiz_progress.id})
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_id": self.answer1_1.id}
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invitation not accepted.")

    def test_quiz_submission_after_already_taken(self):
        # Mark the quiz as passed
        self.quiz_progress.status = QUIZ_PASSED
        self.quiz_progress.save()

        url = reverse("submit-quiz", kwargs={"quiz_progress_id": self.quiz_progress.id})
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_id": self.answer1_1.id}
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Quiz already taken.")
