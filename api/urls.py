from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    NoteList,
    NoteDetail,
)

urlpatterns = [
    path('', NoteList.as_view()),
    path('<uuid:pk>/', NoteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)