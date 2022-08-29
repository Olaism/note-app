from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Note

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user).order_by('-created_on')

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class NoteSearchView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_search.html'
    context_object_name ='notes'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        return queryset.filter(created_by=self.request.user).filter(text__icontains=search).order_by('-created_on')

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ('text',)
    template_name = 'note_form.html'
    
    def form_valid(self, form):
        note = form.save(commit=False)
        note.created_by = self.request.user
        note.save()
        return redirect('note_detail', note.pk)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ('text',)
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('note_list')
    context_object_name = 'note'
    template_name = 'note_delete.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.created_by

    def handle_no_permission(self):
        return JsonResponse(
            {'message': "You are not authorized to access this page"}
        )