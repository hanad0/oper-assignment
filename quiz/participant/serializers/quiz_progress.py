from rest_framework import serializers
from quiz.models import QuizProgress, Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text"]
        read_only_fields = fields


class QuestionWithAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]
        read_only_fields = fields


class DetailedQuizSerializer(serializers.ModelSerializer):
    questions = QuestionWithAnswersSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["title", "slug", "description", "questions"]
        read_only_fields = fields


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["title", "slug", "description"]
        read_only_fields = fields


class QuizProgressSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizProgress
        fields = ["id", "score", "status", "quiz"]
        read_only_fields = ["id"]


class DetailedQuizProgressSerializer(serializers.ModelSerializer):
    quiz = DetailedQuizSerializer(read_only=True)

    class Meta:
        model = QuizProgress
        fields = ["id", "score", "status", "quiz"]
        read_only_fields = ["id"]
