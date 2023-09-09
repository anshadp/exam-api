from rest_framework import serializers
from .models import ExamDetails, Questions, Answers

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDetails
        fields = ('id', 'exam_id', 'exam_type', 'description')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('id', 'answers', 'question', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'exam', 'question', 'mark', 'question_type')


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('id', 'exam', 'question', 'mark', 'question_type', 'answers')