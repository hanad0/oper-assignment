from django.contrib.auth.models import User
from django.test import TestCase
from decimal import Decimal

from quiz.const.quiz_status import QUIZ_INVITED
from quiz.models import QuizProgress, Question, Answer, Quiz
from quiz.util.quiz_score_service import (
    AnswerSubmission,
    QuizScoreContext,
    QuizScoreService,
    QuizScoreResult,
    QuizStatus,
)


class QuizScoreServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="participant", password="password"
        )
        self.quiz = Quiz.objects.create(
            title="Sample Quiz", passing_score_percentage=50.0, created_by=self.user
        )
        self.question1 = Question.objects.create(quiz=self.quiz, text="Question 1")
        self.question2 = Question.objects.create(quiz=self.quiz, text="Question 2")
        self.answer1 = Answer.objects.create(
            question=self.question1, text="Answer 1", is_correct=True
        )
        self.answer2 = Answer.objects.create(
            question=self.question2, text="Answer 2", is_correct=True
        )
        self.quiz_progress = QuizProgress.objects.create(
            quiz=self.quiz, user_id=self.user.id, status=QUIZ_INVITED
        )

    def test_get_score_and_status(self):
        submissions = [
            AnswerSubmission(question_id=self.question1.id, answer_id=self.answer1.id),
            AnswerSubmission(question_id=self.question2.id, answer_id=self.answer2.id),
        ]
        context = QuizScoreContext(
            quiz_progress=self.quiz_progress, quiz_submission=submissions
        )

        result = QuizScoreService.get_score_and_status(context)

        self.assertIsInstance(result, QuizScoreResult)
        self.assertEqual(result.result, Decimal("100.00"))
        self.assertEqual(result.quiz_status, QuizStatus.PASSED)
        self.assertEqual(len(result.answers), 2)
        self.assertTrue(all(answer.is_correct for answer in result.answers))

    def test_get_score_and_status_incorrect_answers(self):
        wrong_answer1_id = self.answer1.id + 1
        wrong_answer2_id = self.answer2.id + 1

        submissions = [
            AnswerSubmission(question_id=self.question1.id, answer_id=wrong_answer1_id),
            AnswerSubmission(question_id=self.question2.id, answer_id=wrong_answer2_id),
        ]
        context = QuizScoreContext(
            quiz_progress=self.quiz_progress, quiz_submission=submissions
        )

        result = QuizScoreService.get_score_and_status(context)

        self.assertIsInstance(result, QuizScoreResult)
        self.assertEqual(result.result, Decimal("0.00"))
        self.assertEqual(result.quiz_status, QuizStatus.FAILED)
        self.assertEqual(len(result.answers), 2)
        self.assertFalse(any(answer.is_correct for answer in result.answers))

    def test_get_score_and_status_mixed_answers(self):
        wrong_answer1_id = self.answer1.id + 1

        submissions = [
            AnswerSubmission(question_id=self.question1.id, answer_id=wrong_answer1_id),
            AnswerSubmission(question_id=self.question2.id, answer_id=self.answer2.id),
        ]
        context = QuizScoreContext(
            quiz_progress=self.quiz_progress, quiz_submission=submissions
        )

        result = QuizScoreService.get_score_and_status(context)

        self.assertIsInstance(result, QuizScoreResult)
        self.assertEqual(result.result, Decimal("50.00"))
        self.assertEqual(result.quiz_status, QuizStatus.PASSED)
        self.assertEqual(len(result.answers), 2)
