from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteSearchView

User = get_user_model()


class NoteSearchViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@example.com',
            password = 'testpassword'
        )
        self.note = Note.objects.create(
            text='Wow!',
            created_by=self.user
        )
        self.url = reverse('note_search')
        self.client.login(username='testuser', password='testpassword')

class NoteSearchNoQueryViewTest(NoteSearchViewTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/notes/search/')
        self.assertEquals(view.func.view_class, NoteSearchView)

    def test_search_results_heading(self):
        self.assertContains(self.response, 'Results for "All"')

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'note_search.html')

class NoteSearchQueryNotFoundViewTest(NoteSearchViewTestCase):

    def setUp(self):
        super().setUp()
        url = reverse('note_search') + '?q=nothing'
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_search_results_heading(self):
        self.assertContains(self.response, 'There are no results for "nothing"')

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'note_search.html')

class NoteSearchQueryFoundViewTest(NoteSearchViewTestCase):

    def setUp(self):
        super().setUp()
        url = reverse('note_search') + '?q=Wow'
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_search_results_heading(self):
        self.assertContains(self.response, 'Results for "Wow"')

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'note_search.html')


class NoteSearchLoginRedirectTest(TestCase):

    def setUp(self):
        self.url = reverse('note_search')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('account_login')
        self.assertRedirects(self.response, f"{login_url}?next={self.url}")