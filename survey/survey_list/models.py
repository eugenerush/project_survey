from django.db import models
from django.core.exceptions import ValidationError


def question_type_validator(value):
    if not value in ['question_id', 'One_Choice', 'Any_Choice']:
        raise ValidationError('Неверный тип вопроса')


OPTION_TYPES = ['One_Choice', 'Any_Choice']


class Survey(models.Model):
    title = models.CharField(verbose_name='Название', unique=True, db_index=True, max_length=128)
    start_data = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    end_data = models.DateTimeField(verbose_name='Дата окончания', auto_now_add=False)
    description = models.CharField(verbose_name='Описание', db_index=True, max_length=256)


class Question(models.Model):
    survey_title = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.CharField(verbose_name='Вопрос', max_length=256)
    type = models.CharField(max_length=30, validators=[question_type_validator])

    @property
    def answer_type(self):
        return self.type in OPTION_TYPES


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    answer = models.CharField(verbose_name='Ответ', max_length=128)


class Submit(models.Model):
    user_id = models.IntegerField(verbose_name='Пользователь', db_index=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(verbose_name='Время выполнения', auto_now_add=True)


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submit, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=30, validators=[question_type_validator])
    question_text = models.CharField(verbose_name='Текст вопроса', max_length=300)
    answer = models.CharField(verbose_name='Ответ', max_length=256)
