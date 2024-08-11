from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from quiz.models import Quiz


class QuizViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        group = Group.objects.get(name="quiz_creator")
        self.user.groups.add(group)
        self.client.login(username="testuser", password="testpass")

        self.quiz = Quiz.objects.create(
            title="Sample1 Quiz",
            description="Sample Description",
            slug="sample-quiz",
            created_by=self.user,
        )

        Quiz.objects.create(
            title="Sample2 Quiz",
            description="Sample Description",
            slug="sample-quiz-2",
            created_by=self.user,
        )

    def test_list_quizzes(self):
        response = self.client.get(reverse("creator-quiz-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_retrieve_quiz(self):
        response = self.client.get(reverse("creator-quiz-detail", args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertIn("questions", response.data)

    def test_filter_quizzes(self):
        response = self.client.get(
            reverse("creator-quiz-list"), {"slug": "sample-quiz"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["slug"], "sample-quiz")

    def test_search_quizzes(self):
        response = self.client.get(reverse("creator-quiz-list"), {"search": "Sample1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.quiz.title)

    def test_order_quizzes(self):
        # Assuming there's more than one quiz
        response = self.client.get(
            reverse("creator-quiz-list"), {"ordering": "-created_at"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(
            response.data["results"][0]["created_at"],
            response.data["results"][1]["created_at"],
        )

    def test_permissions(self):
        User.objects.create_user(username="otheruser", password="testpass")
        self.client.login(username="otheruser", password="testpass")
        response = self.client.get(reverse("creator-quiz-detail", args=[self.quiz.id]))
        self.assertEqual(response.status_code, 403)
