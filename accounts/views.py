from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'my_account.html'
    fields = ('profile_pic', 'first_name', 'last_name', 'email',)
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user