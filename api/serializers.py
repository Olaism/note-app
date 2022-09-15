from django.contrib.auth import get_user_model

from rest_framework import serializers

from note.models import Note

class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Note
        fields = ('id', 'text', 'created_by', 'created_on', 'modified_on')