from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.NoteListView.as_view(), name='note_list'),
    path('<uuid:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('new/', views.NoteCreateView.as_view(), name='note_create'),
    path('<uuid:pk>/update/', views.NoteUpdateView.as_view(), name='note_update'),
    path('<uuid:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('search/', views.NoteSearchView.as_view(), name='note_search'),
]