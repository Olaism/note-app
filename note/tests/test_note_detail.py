from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteDetailView

class GlobalTestCase(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
                    username='testuser', 
                    email='testuser@example.com', 
                    password='testpassword',
                )

        self.note = Note.objects.create(
                    text = 'This is my note',
                    created_by = self.user,
                )

class LoginRequiredNoteDetailView(GlobalTestCase):

    def test_permission_denied_status_code_when_logged_out(self):
        response = self.client.get(self.note.get_absolute_url())
        self.assertEquals(response.status_code, 403)

class NoteDetailTestCase(GlobalTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.note.get_absolute_url()

class NoteDetailViewTest(NoteDetailTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password='testpassword')
        
        self.response = self.client.get(self.url)

    def test_user_authentication(self):
        user = self.response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_loggedin_user(self):
        user = self.response.context.get('user')
        self.assertEquals(self.user, user)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve(f'/notes/{self.note.pk}/')
        self.assertEquals(view.func.view_class, NoteDetailView)

    def test_contains_neccessary_links_and_texts(self):
        home_link = reverse('note_list')
        update_link = reverse('note_update', kwargs={'pk': self.note.pk})
        delete_link = reverse('note_delete', kwargs={'pk': self.note.pk})
        profile_link = reverse('my_account')
        change_password_link = reverse('password_change')
        logout_link = reverse('logout')
        user = self.response.context.get('user')
        self.assertContains(self.response, home_link)
        self.assertContains(self.response, update_link)
        self.assertContains(self.response, delete_link)
        self.assertContains(self.response, self.note.text)
        self.assertContains(self.response, profile_link)
        self.assertContains(self.response, change_password_link)
        self.assertContains(self.response, logout_link)
        self.assertContains(self.response, user.username)

    def test_does_not_contains_unneccessary_links_and_texts(self):
        self.assertNotContains(self.response, 'type="search"')

class UnauthorizedNoteDetailView(NoteDetailTestCase):

    def setUp(self):
        super().setUp()
        unauthorized_user = get_user_model().objects.create_user(
            username = 'testuser02',
            password = 'testpassword02',
            email='testuser02@example.com'
        )
        self.client.login(username = 'testuser02', password = 'testpassword02')

    def test_permission_denied_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 403)