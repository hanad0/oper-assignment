from typing import List, Dict
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from dataclasses import dataclass

from quiz.const.quiz_status import QUIZ_FAILED, QUIZ_PASSED
from quiz.models import QuizProgress, UserAnswer


@dataclass
class AnswerSubmission:
    question_id: int
    answer_id: int


@dataclass
class QuizScoreContext:
    quiz_progress: QuizProgress
    quiz_submission: List[AnswerSubmission]


class QuizStatus(Enum):
    FAILED = QUIZ_FAILED
    PASSED = QUIZ_PASSED


@dataclass
class QuizScoreResult:
    result: Decimal
    quiz_status: QuizStatus
    answers: List[UserAnswer]


class QuizScoreService:

    @staticmethod
    def get_score_and_status(context: QuizScoreContext) -> QuizScoreResult:
        quiz = context.quiz_progress.quiz
        quiz_submission = context.quiz_submission

        correct_answer_dict = QuizScoreService._get_correct_answers(quiz)
        submitted_answer_dict = QuizScoreService._get_submitted_answers(quiz_submission)

        correct_answer_count, answer_results = QuizScoreService._evaluate_answers(
            correct_answer_dict, submitted_answer_dict, context.quiz_progress.id
        )

        score = QuizScoreService._calculate_score(
            correct_answer_count, len(correct_answer_dict)
        )
        status = QuizScoreService._determine_status(
            score, quiz.passing_score_percentage
        )

        return QuizScoreResult(result=score, quiz_status=status, answers=answer_results)

    @staticmethod
    def _get_correct_answers(quiz) -> Dict[int, set]:
        """Return a dictionary mapping question IDs to sets of correct answer IDs."""
        return {
            question.id: {
                answer.id for answer in question.answers.all() if answer.is_correct
            }
            for question in quiz.questions.all()
        }

    @staticmethod
    def _get_submitted_answers(submissions: List[AnswerSubmission]) -> Dict[int, int]:
        """Return a dictionary mapping question IDs to submitted answer IDs."""
        return {
            submission.question_id: submission.answer_id for submission in submissions
        }

    @staticmethod
    def _evaluate_answers(
        correct_answer_dict: Dict[int, set],
        submitted_answer_dict: Dict[int, int],
        user_quiz_id: int,
    ) -> tuple:
        """Evaluate answers and return correct answer count and list of AnswerResult instances."""
        correct_answer_count = 0
        answer_results = []

        for question_id, correct_answers in correct_answer_dict.items():
            submitted_answer = submitted_answer_dict.get(question_id)
            is_correct = submitted_answer in correct_answers
            if is_correct:
                correct_answer_count += 1

            answer_results.append(
                UserAnswer(
                    question_id=question_id,
                    answer_id=submitted_answer,
                    user_quiz_id=user_quiz_id,
                    is_correct=is_correct,
                )
            )

        return correct_answer_count, answer_results

    @staticmethod
    def _calculate_score(correct_answer_count: int, total_questions: int) -> Decimal:
        """Calculate and return the score rounded to two decimal places."""
        score = (Decimal(correct_answer_count) / total_questions) * 100
        return score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def _determine_status(
        score: Decimal, passing_score_percentage: Decimal
    ) -> QuizStatus:
        """Determine the quiz status based on the score and passing percentage."""
        return (
            QuizStatus.PASSED
            if score >= passing_score_percentage
            else QuizStatus.FAILED
        )
