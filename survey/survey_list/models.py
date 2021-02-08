from django.db import models


class Survey(models.Model):
    title = models.CharField(verbose_name='Название', unique=True, db_index=True, max_length=64)
    start_data = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    end_data = models.DateTimeField(verbose_name='Дата окончания', auto_now_add=False)
    description = models.CharField(verbose_name='Описание', db_index=True, max_length=256)


class Question(models.Model):
    survey_title = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.CharField(verbose_name='Вопрос', max_length=256)


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='Ответ', max_length=256)
    result = models.BooleanField('Результат', default=False)
