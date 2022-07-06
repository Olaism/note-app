from django.test import TestCase, SimpleTestCase
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteCreateView

class LoginRequiredNoteCreateGetMethodView(SimpleTestCase):
    def test_redirection(self):
        url = reverse('note_create')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{0}?next={1}'.format(login_url, url))

class NoteCreateGetMethodViewTest(TestCase):

    def setUp(self):

        user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@gmail.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note_create')
        self.response = self.client.get(url)

    def check_authentication(self):
        user = self.response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve('/notes/new/')
        self.assertEquals(view.func.view_class, NoteCreateView)

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
        note_create_link = reverse('note_create')
        self.assertNotContains(self.response, '{0}'.format(note_create_link))

class NoteCreatePostMethodViewTestCase(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpassword'
        )
        self.unauthorized_user = get_user_model().objects.create(
            username='testuser02', 
            email='testuser02@gmail.com',
            password='testpassword02'
        )
        self.url = reverse('note_create')
        # self.response = self.client.post(url, data)

class NoteCreateSuccessfulPostMethodViewTest(NoteCreatePostMethodViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.post(self.url, {
            'text': 'Lorem ipsum dolor sit amet',
            'created_by': self.user
        })

    def test_redirection_status_code(self):
        self.assertEquals(self.response.status_code, 302)

    def test_note_creation(self):
        self.assertTrue(Note.objects.exists())

class NoteCreateInvalidPostMethodViewTest(NoteCreatePostMethodViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_note_not_created(self):
        self.assertFalse(Note.objects.exists())