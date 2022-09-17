from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Note
from ..views import NoteListView

class NoteListRedirectView(SimpleTestCase):

    def test_redirection(self):
        url = reverse('note_list')
        login_url = reverse('account_login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, f"{login_url}?next={url}")

class NoteListTest(TestCase):

    username = 'testuser'
    password = 'testpassword'

    def setUp(self):
        self.url = reverse('note_list')
        self.user = get_user_model().objects.create_user(
            username=self.username,
            email='testuser@example.com',
            password=self.password
        )
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_note_list_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_note_list_view_url_resolves_correct_view(self):
        view = resolve('/notes/all/')
        self.assertEquals(view.func.view_class, NoteListView)

    def test_note_list_view_contains_correct_links(self):
        link_to_profile = reverse('my_account')
        link_to_password_change = reverse('account_change_password')
        link_to_logout = reverse('account_logout')
        link_to_create_new_note = reverse('note_create')
        self.assertContains(self.response, link_to_profile)
        self.assertContains(self.response, link_to_password_change)
        self.assertContains(self.response, link_to_logout)
        self.assertContains(self.response, link_to_create_new_note)

    def test_no_note_response(self):
        self.assertContains(self.response, 'There are no notes yet.')

    def test_note_list_view_does_not_contain_links(self):
        link_to_login = reverse('account_login')
        link_to_signup = reverse('account_signup')
        self.assertNotContains(self.response, link_to_login)
        self.assertNotContains(self.response, link_to_signup)

    def test_search_form(self):
        self.assertContains(self.response, 'type="search"')
        self.assertContains(self.response, '<input', 1)

    def test_querysets(self):
        notes = self.response.context.get('notes')
        self.assertFalse(notes)
        self.assertEquals(len(notes), 0)

class NoteListNoteCreationTest(TestCase):
    
    def setUp(self):
        url = reverse('note_list')
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        self.note = Note.objects.create(
            text="Lorem ipsum dolor sit amet, consectet",
            created_by=user,
        )
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(url)

    def test_note_creation_required_links(self):
        edit_note_link = reverse('note_update', kwargs={'pk':self.note.pk})
        delete_note_link = reverse('note_delete', kwargs={'pk': self.note.pk})
        note_details_link = reverse('note_detail', kwargs={'pk':self.note.pk})
        note_create_link = reverse('note_create')
        self.assertContains(self.response, edit_note_link)
        self.assertContains(self.response, delete_note_link)
        self.assertContains(self.response, note_details_link)
        self.assertContains(self.response, note_create_link)

    def test_querysets(self):
        notes = self.response.context['notes']
        self.assertTrue(notes)
        self.assertEquals(len(notes), 1)