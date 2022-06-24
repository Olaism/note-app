from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Note

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user).order_by('-created_on')

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ('text',)
    template_name = 'note_form.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user).order_by('-created_on')
    
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note_list')
    context_object_name = 'note'
    template_name = 'note_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)