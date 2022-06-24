from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('note.urls')),
    path('', RedirectView.as_view(url='/notes/all/')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]