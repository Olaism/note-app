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
    path('api/v1/account/', include('dj_rest_auth.urls')),
    path('api/v1/account/register/', include('dj_rest_auth.registration.urls')),
    path('api/v1/', include('api.urls')),
    path('', RedirectView.as_view(url='/notes/all/')),
    path('profile/', UserUpdateView.as_view(), name='my_account'),
    path('account/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # urlpatterns = [
    # path('__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns