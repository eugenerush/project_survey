from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import ParseError
from django.http import Http404
from datetime import date
from django.contrib import admin

from .models import Survey, Question, AnswerOption, question_type_validator
from .serializers import SurveySerializer, QuestionSerializer, AnswerOptionSerializer


class AdminAPIView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]


class AdminSurveys(AdminAPIView):
    def get(self, request):
        return Response(SurveySerializer(Survey.objects.all(), many=True).data)

    def post(self, request):
        try:
            s = SurveySerializer(data=request.data)
            s.is_valid(raise_exception=True)
            d = s.validated_data
            if d['start_data'] > d['end_data']:
                raise Exception('Invalid end_data')

            new_survey = Survey(**d)
            new_survey.save()
            return Response(SurveySerializer(new_survey).data)
        except Exception as ex:
            raise ParseError(ex)


class AdminSurveyById(AdminAPIView):
    def get(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            result = SurveySerializer(survey).data
            result['questions'] = []
            for question in survey.question_set.all():
                question_dict = QuestionSerializer(question).data
                if question.answer_type:
                    question_dict['answers'] = AnswerOptionSerializer(question.answer_set.all(), many=True).data
                result['questions'].append(question_dict)

            return Response(result)

        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def delete(self, request, id):
        try:
            Survey.objects.get(id=id).delete()
            return Response('Deleted')
        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def patch(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            d = request.data
            if 'name' in d:
                survey.name = d['name']
            if 'description' in d:
                survey.description = d['description']
            if 'end_data' in d:
                survey.end_data = date.fromisoformat(d['end_data'])

            if survey.start_data > survey.end_data:
                raise Exception('Invalid end_data')

            survey.save()
            return Response(SurveySerializer(survey).data)

        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class AdminQuestions(AdminAPIView):
    def post(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            qs = QuestionSerializer(data=request.data)
            qs.is_valid(raise_exception=True)
            pd = dict(qs.validated_data)
            pd['survey'] = survey
            new_question = Question(**pd)

            require_answers = new_question.answer_type
            new_answer_list = []
            if require_answers:
                if not 'answers' in request.data:
                    raise Exception('answers are missing')
                if type(request.data['answers']) != list or len(request.data['answers']) < 2:
                    raise Exception('Invalid answers')

                index = 1
                for answer in request.data['answers']:
                    new_answer_list.append(AnswerOption(
                        answer=answer,
                        index=index
                    ))
                    index += 1

            new_question.save()
            if require_answers:
                for new_answer in new_answer_list:
                    new_answer.question = new_question
                    new_answer.save()

            result = QuestionSerializer(new_question).data
            if require_answers:
                result['answers'] = [AnswerOptionSerializer(o).data for o in new_answer_list]

            return Response(result)

        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class AdminQuestionById(AdminAPIView):
    def get(self, request, survey_id, question_id):
        try:
            question = Question.objects.get(id=question_id)
            result = QuestionSerializer(question).data
            if question.answer_type:
                result['answers'] = AnswerOptionSerializer(question.answer_set.all(), many=True)
            return Response(result)

        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def delete(self, request, survey_id, question_id):
        try:
            Question.objects.get(id=question_id).delete()
            return Response('Deleted')
        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def patch(self, request, survey_id, question_id):
        try:
            delete_existing_answers = False
            require_new_answer = False
            prev_question = Question.objects.get(id=question_id)
            next_question = Question.objects.get(id=question_id)
            d = request.data
            if 'answer' in d:
                next_question.answer = d['answer']
            if 'type' in d:
                question_type_validator(d['type'])
                next_question.type = d['type']

            if prev_question.answer_type and not next_question.answer_type:
                delete_existing_answers = True
            if not prev_question.answer_type and next_question.answer_type:
                require_new_answer = True
            if prev_question.answer_type and next_question.answer_type and 'answers' in d:
                delete_existing_answers = require_new_answer = True

            if require_new_answer:
                if not 'answers' in d:
                    raise Exception('answers are missing')
                if type(d['answers']) != list or len(d['answers']) < 2:
                    raise Exception('Invalid answers')

            if delete_existing_answers:
                AnswerOption.objects.filter(question=next_question).delete()

            if require_new_answer:
                index = 1
                for answer in d['answers']:
                    AnswerOption(answer=answer, index=index, question=next_question).save()
                    index += 1

            next_question.save()

            result = QuestionSerializer(next_question).data
            if next_question.answer_type:
                result['answers'] = AnswerOptionSerializer(next_question.answer_set.all(), many=True).data

            return Response(result)

        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


admin.site.register(Survey)
admin.site.register(Question)

