from django.urls import path
from .views import UploadDocumentView, AskQuestionView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view()),
    path('ask-question/', AskQuestionView.as_view()),
]
