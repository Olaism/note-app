from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('note.urls')),
    path('', RedirectView.as_view(url='/notes/all/')),
]