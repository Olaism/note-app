from rest_framework import generics

from note.models import Note
from .permissions import IsNoteCreator
from .serializers import NoteSerializer


class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsNoteCreator,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer