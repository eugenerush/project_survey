from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SurveyDetailSerializer, QuestionDetailSerializer, AnswerDetailSerializer, SurveyListSerializer
from .models import Survey, Question


class SurveyCreateView(generics.CreateAPIView):
    serializer_class = SurveyDetailSerializer


class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionDetailSerializer


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerDetailSerializer


class SurveyListView(generics.ListAPIView):
    serializer_class = SurveyListSerializer
    queryset = Survey.objects.all()


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveyDetailSerializer
    queryset = Survey.objects.all()


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()


class IndexView(generics.ListAPIView):
    serializer_class = SurveyListSerializer
    template_name = 'index.html'
    context_object_name = 'survey_list'
    queryset = Survey.objects.all()
