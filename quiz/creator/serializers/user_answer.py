from rest_framework import serializers

from quiz.creator.serializers.answer import AnswerSerializer
from quiz.creator.serializers.question import QuestionSerializer
from quiz.models import UserAnswer


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ["question", "answer"]
        read_only_fields = fields
