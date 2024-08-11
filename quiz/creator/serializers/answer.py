from rest_framework import serializers
from quiz.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "is_correct", "created_at"]
        read_only_fields = ["id", "created_at"]
