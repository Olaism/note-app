from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    text = models.TextField(max_length=4000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        # slugify_text = slugify(self.text)
        return self.text[20]