from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'survey'

urlpatterns = [
    path('survey/create/', SurveyCreateView.as_view()),
    path('question/create/', QuestionCreateView.as_view()),
    path('answer/create/', AnswerCreateView.as_view()),
    path('survey-list/', SurveyListView.as_view()),
    path('survey/detail/<int:pk>/', SurveyDetailView.as_view()),
    path('question/detail/<int:pk>/', QuestionDetailView.as_view()),
    path('index', IndexView.as_view(), name='index'),
]
