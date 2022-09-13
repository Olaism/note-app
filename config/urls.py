# import debug_toolbar
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import SignUpView, UserUpdateView

urlpatterns = [
    path('olaism-admin/', admin.site.urls),
    path('notes/', include('note.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/notes/', include('api.urls')),
    path('', RedirectView.as_view(url='/notes/all/')),
    path('profile/', UserUpdateView.as_view(), name='my_account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('settings/password/change/', views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('settings/password/change/done/', views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password/reset/', views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
        ), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/success/', views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # urlpatterns = [
    # path('__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns