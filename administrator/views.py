from django.shortcuts import render
from administrator.models import ExamDetails, Questions
from administrator.serializers import ExamSerializer, QuestionSerializer, AnswerSerializer, QuestionWithAnswerSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework import status

# Create your views here.


class ExamsDetails(APIView):
    """
    List all exam, or create a new Exam.
    """
    def get(self, request, format=None):
        questions = ExamDetails.objects.all()
        serializer = ExamSerializer(questions, many=True)
        return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "New exam created", "data": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetails(APIView):
    """
    Retrieve, update or delete a question instance.
    """
    def get_object(self, pk=None):
        try:
            return Questions.objects.all()
        except Questions.DoesNotExist:
            raise Http404

    def get(self, request, format=None, pk=None):
        if pk:
            questions = self.get_object(pk)
        questions = Questions.objects.all()
        serializer = QuestionWithAnswerSerializer(questions, many=True)
        return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)    

    def post(self, request, format=None):
        question_data = {'question': request.data.get('question')}
        print('question_data', question_data)

        question_serializer = QuestionSerializer(data=question_data['question'])
        if question_serializer.is_valid():
            question = question_serializer.save()
        else:
            return JsonResponse({"status": "error", "data": question_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if question.question_type == 3 or question.question_type == 2:
            answer_data = {'answer': request.data.get('answer')}

            if isinstance(answer_data['answer'], list):
                for answer in answer_data['answer']:
                    data = {'answers': answer['answer'], 'is_correct':  answer['is_correct'], 'question': question.id}
                    answer_serializer = AnswerSerializer(data=data)

                    if answer_serializer.is_valid():
                        answer = answer_serializer.save()
                    else:
                        question.delete()
                        return JsonResponse({"status": "error", "data": answer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                question.delete()
                return JsonResponse({"status": "error", "data": 'multiple choice question must have list of items'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            answer_data = {'answer': request.data.get('answer'), 'question': question.id}

            answer_serializer = AnswerSerializer(data=answer_data)
            if answer_serializer.is_valid():
                answer = answer_serializer.save()
            else:
                question.delete()
                return JsonResponse({"status": "error", "data": answer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        return JsonResponse({'question': question_serializer.data, 'answer': answer_serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return JsonResponse({"status": "data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)