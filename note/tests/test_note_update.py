from django.test import TestCase, SimpleTestCase
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteUpdateView

class LoginRequiredNoteUpdateGetMethodView(SimpleTestCase):
    def test_redirection(self):
        url = reverse('note_create')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{0}?next={1}'.format(login_url, url))

class NoteUpdateGetMethodViewTest(TestCase):

    def setUp(self):

        user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@gmail.com',
            password='testpassword'
        )
        self.note = Note.objects.create(text='Lorem ipsum dolor sit amet, consectetur adipiscing elit', created_by=user)
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('note_update', kwargs={'pk': self.note.pk})
        self.response = self.client.get(self.url)

    def check_authentication(self):
        user = self.response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve(f'{self.url}')
        self.assertEquals(view.func.view_class, NoteUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_contains_link_back_to_homepage(self):
        homelink = reverse('note_list')
        self.assertContains(self.response, '{0}'.format(homelink))

    def test_does_not_contain_link_to_itself(self):
        note_update_link = reverse('note_update', kwargs={'pk': self.note.pk})
        self.assertNotContains(self.response, '{0}'.format(note_update_link))

class NoteUpdatePostMethodViewTestCase(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpassword'
        )
        self.note = Note.objects.create(
            text="Lorem Ipsum",
            created_by=self.user
        )
        self.url = reverse('note_update', kwargs={'pk': self.note.pk})
        # self.response = self.client.post(url, data)

class NoteUpdateSuccessfulPostMethodViewTest(NoteUpdatePostMethodViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.post(self.url, {
            'text': 'Lorem ipsum dolor sit amet(updated)',
        })

    def test_redirection_status_code(self):
        self.assertEquals(self.response.status_code, 302)

    def test_note_update(self):
        self.note.refresh_from_db()
        self.assertEquals(self.note.text, 'Lorem ipsum dolor sit amet(updated)')

class NoteUpdateInvalidPostMethodViewTest(NoteUpdatePostMethodViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_note_not_updated(self):
        self.note.refresh_from_db()
        self.assertEquals(self.note.text, 'Lorem Ipsum')