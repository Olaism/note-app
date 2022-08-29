import uuid
from django.urls import reverse
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from markdown import markdown

class Note(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    text = models.TextField(max_length=4000)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="notes")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def get_text_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))

    def __str__(self):
        # slugify_text = slugify(self.text)
        return self.text[20]

    def get_absolute_url(self):
        return reverse('note_detail', args=[str(self.pk)])