from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import serializers

from quiz.creator.serializers.question import QuestionWithAnswersSerializer
from quiz.models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "passing_score_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        if "slug" not in validated_data:
            validated_data["slug"] = slugify(validated_data["title"])
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if "slug" in str(e) and "unique" in str(e):
                raise serializers.ValidationError(
                    {"slug": ["Quiz with this slug already exists."]}
                )
            else:
                raise e


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionWithAnswersSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "passing_score_percentage",
            "created_at",
            "updated_at",
            "questions",
        ]
        read_only_fields = fields
