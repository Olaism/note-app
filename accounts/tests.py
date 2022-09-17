from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from accounts.views import UserUpdateView

User = get_user_model()

class LoginRequiredUserUpdateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('my_account')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('account_login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')


class UserUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        url = reverse('my_account')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_to_correct_view(self):
        view = resolve('/profile/')
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'my_account.html')

    def test_csrf_protection(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, '>Update</button>', 1)


class UserUpdatePostViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        url = reverse('my_account')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.post(url, {'first_name': 'test', 'last_name': 'user'})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('my_account'))