from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import Http404
from datetime import date
import json

from .models import Survey, Submit, Answer
from .serializers import SurveySerializer, QuestionSerializer, UserAnswerOptionSerializer, SubmitSerializer


class Surveys(APIView):
    def get(self, request):
        today = date.today()
        survey_set = Survey.objects.filter(start_data__lte=today, end_data__gt=today)
        return Response(SurveySerializer(survey_set, many=True).data)


class SurveyById(APIView):
    def get(self, request, id):
        try:
            today = date.today()
            survey = Survey.objects.get(id=id)
            if survey.start_data > today or survey.end_date < today:
                raise Survey.DoesNotExist()

            result = SurveySerializer(survey).data
            result['questions'] = []
            for question in survey.question_set.all():
                question_dict = QuestionSerializer(question).data
                if question.hasOptionType:
                    question_dict['options'] = UserAnswerOptionSerializer(question.option_set.all(), many=True).data
                result['questions'].append(question_dict)

            return Response(result)

        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def post(self, request, id):
        try:
            today = date.today()
            survey = Survey.objects.get(id=id)
            if survey.start_data > today or survey.end_data < today:
                raise Survey.DoesNotExist()

            if not 'user_id' in request.data:
                raise Exception('userId is missing')
            if not type(request.data['user_id']) is int:
                raise Exception('Invalid user_id')
            if not 'answers' in request.data:
                raise Exception('answers are missing')
            if not type(request.data['answers']) is dict:
                raise Exception('Invalid answers')

            user_id = request.data['user_id']
            answer_dict = request.data['answers']

            if Submit.objects.filter(userId=user_id, survey=survey).count() > 0:
                raise Exception('This user already has submitted to this survey')

            def make_answer(question):
                if not str(question.id) in answer_dict:
                    raise Exception('Answer to question %d is missing' % question.id)

                answer_data = answer_dict[str(question.id)]
                answer = Answer(
                    question=question,
                    questionType=question.type,
                    question_id=question.text)

                invalidAnswerException = Exception('Invalid answer to question %d' % question.id)
                invalidIndexException = Exception('Invalid option index in answer to question %d' % question.id)
                if question.type == 'question_id':
                    if not type(answer_data) is str:
                        raise invalidAnswerException
                    answer.answerText = answer_data

                if question.type == 'One_Choice':
                    if not type(answer_data) is int:
                        raise invalidAnswerException
                    foundOption = question.option_set.filter(index=answer_data).first()
                    if foundOption:
                        answer.answerText = foundOption.text
                    else:
                        raise invalidIndexException

                if question.type == 'Any_Choice':
                    if not type(answer_data) is list:
                        raise invalidAnswerException
                    optionList = question.option_set.all()
                    resultList = []
                    for index in answer_data:
                        foundOption = next((o for o in optionList if o.index == index), None)
                        if foundOption:
                            resultList.append(foundOption.text)
                        else:
                            raise invalidIndexException
                    answer.answerText = json.dumps(resultList)

                return answer

            answerList = [make_answer(question) for question in survey.question_set.all()]
            if len(answerList) != survey.question_set.count():
                raise Exception('Not enough answers')

            submis = Submit(userId=user_id, survey=survey)
            submis.save()
            for answer in answerList:
                answer.submission = submis
                answer.save()

            return Response('Accepted')

        except Survey.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class SurveysByUser(APIView):
    def get(self, request, id):
        try:
            result = []
            for submission in Submit.objects.filter(user_id=id).order_by('submitTime'):
                submissionDict = SubmitSerializer(submission).data
                submissionDict['survey_id'] = submission.survey_id
                submissionDict['answers'] = []
                for answer in submission.answer_set.all():
                    answerText = answer.answerText
                    if answer.questionType == 'Any_Choice':
                        answerText = json.loads(answerText)

                    submissionDict['answers'].append({
                        'question': {
                            'id': answer.question_id,
                            'type': answer.questionType,
                            'text': answer.questionText
                        },
                        'answer': answerText
                    })

                result.append(submissionDict)

            return Response(result)

        except Exception as ex:
            raise ParseError(ex)