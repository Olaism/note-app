from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views

from accounts.views import SignUpView, UserUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('note.urls')),
    path('', RedirectView.as_view(url='/notes/all/')),
    path('profile/', UserUpdateView.as_view(), name='my_account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('settings/password/change/', views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('settings/password/change/done/', views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]