from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    APIHome,
    NoteList,
    NoteDetail,
    NoteCreate,
    NoteUpdate,
    NoteDelete,
)

app_name = 'api'

urlpatterns = [
    path('notes/', NoteList.as_view()),
    path('home/', APIHome.as_view(), name='home'),
    path('notes/<uuid:pk>/', NoteDetail.as_view()),
    path('notes/create/', NoteCreate.as_view()),
    path('notes/<uuid:pk>/edit/', NoteUpdate.as_view()),
    path('notes/<uuid:pk>/delete/', NoteDelete.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)