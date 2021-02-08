from django.contrib import admin
from django.urls import path, include
from .admin import AdminSurveys, AdminSurveyById, AdminQuestions, AdminQuestionById
from .user import Surveys, SurveyById, SurveysByUser

app_name = 'survey'

urlpatterns = [
    path('surveys', Surveys.as_view()),
    path('surveys/<int:id>', SurveyById.as_view()),
    path('surveysByUser/<int:id>', SurveysByUser.as_view()),
    path('admin/', include([
        path('surveys', AdminSurveys.as_view()),
        path('surveys/<int:id>', AdminSurveyById.as_view()),
        path('surveys/<int:id>/questions', AdminQuestions.as_view()),
        path('surveys/<int:pollId>/questions/<int:questionId>', AdminQuestionById.as_view())
    ]))
]
