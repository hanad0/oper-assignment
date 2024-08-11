from rest_framework import serializers


class AnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class QuizSubmissionSerializer(serializers.Serializer):
    answers = AnswerSubmissionSerializer(many=True)
