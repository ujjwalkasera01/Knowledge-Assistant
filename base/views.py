from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Document
from .serializers import DocumentSerializer, QuestionSerializer
from .utils.loader import process_and_store
from .utils.rag import retrieve_answer

class UploadDocumentView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            doc = serializer.save()
            process_and_store(doc.file.path, doc.title)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AskQuestionView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            answer, sources = retrieve_answer(serializer.validated_data['question'])
            return Response({"answer": answer, "sources": sources})
        return Response(serializer.errors, status=400)
