from django.contrib import admin
from .models import Survey, Question, Answer


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['title', 'description', 'end_data']}
         ),
    ]
    inlines = [QuestionInline]


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['survey_title', 'question_id']}
         ),
    ]
    inlines = [AnswerInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
