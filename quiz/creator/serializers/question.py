from rest_framework import serializers

from quiz.creator.serializers.answer import AnswerSerializer
from quiz.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "created_at"]
        read_only_fields = ["id", "created_at"]


class QuestionWithAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "created_at", "answers"]
        read_only_fields = fields
