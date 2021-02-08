from rest_framework import serializers
from rest_framework.serializers import ValidationError


def question_type_validator(value):
    if not value in ['question_id', 'One_Choice', 'Any_Choice']:
        raise ValidationError('Неверный тип вопроса')


class SurveySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=128)
    start_data = serializers.DateTimeField()
    end_data = serializers.DateTimeField()
    description = serializers.CharField(max_length=256)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    question_id = serializers.CharField(max_length=256)
    type = serializers.CharField(max_length=30, validators=[question_type_validator])


class AnswerOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    index = serializers.IntegerField()
    answer = serializers.CharField(max_length=128)


class UserAnswerOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    index = serializers.IntegerField()
    answer = serializers.CharField(max_length=128)


class SubmitSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    submit_time = serializers.DateTimeField()
