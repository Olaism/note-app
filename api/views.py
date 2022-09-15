from django.views.generic import TemplateView
from rest_framework import generics

from note.models import Note
from .permissions import IsNoteCreator
from .serializers import NoteSerializer

class APIHome(TemplateView):
    template_name = 'api/home.html'


class NoteList(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(created_by=user)

class NoteDetail(generics.RetrieveAPIView):
    permission_classes = (IsNoteCreator,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(created_by=user)

class NoteCreate(generics.CreateAPIView):
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class NoteUpdate(generics.UpdateAPIView):
    permission_classes = (IsNoteCreator,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(created_by=user)

class NoteDelete(generics.DestroyAPIView):
    permission_classes = (IsNoteCreator,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(created_by=user)