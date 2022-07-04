from django.urls import reverse, resolve
from django.test import TestCase
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteDeleteView

class NoteDeleteTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        self.note = Note.objects.create(
            text = 'Lorem ipsum dolor sit amet, consectetur adip',
            created_by=user
        )

        self.url = reverse('note_delete', kwargs={'pk': self.note.pk})

class NoteDeleteViewTest(NoteDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, NoteDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_submit_btn(self):
        self.assertContains(self.response, 'type="submit', 1)