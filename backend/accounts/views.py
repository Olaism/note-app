from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import AccountCreationForm


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = AccountCreationForm
    success_url = reverse_lazy('login')