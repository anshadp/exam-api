from django.urls import path
from . import views

urlpatterns = [
    path('exam-details/',views.ExamsDetails.as_view()),
    path('question-details/',views.QuestionDetails.as_view()),
    path('question-details/<int:pk>',views.QuestionDetails.as_view()),


]