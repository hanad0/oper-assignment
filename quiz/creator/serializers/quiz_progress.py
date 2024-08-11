from rest_framework import serializers

from quiz.creator.serializers import QuizSerializer
from quiz.creator.serializers.user import UserSerializer
from quiz.creator.serializers.user_answer import UserAnswerSerializer
from quiz.models import QuizProgress


class QuizProgressSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuizProgress
        fields = ["id", "score", "status", "quiz", "user"]
        read_only_fields = fields


class DetailedQuizProgressSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    user_answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizProgress
        fields = ["id", "score", "status", "quiz", "user", "user_answers"]
        read_only_fields = fields
