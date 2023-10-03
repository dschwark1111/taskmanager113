from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import(
    ListView,
    DetailView,
    CreateView, 
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy 
from .models import Issue 
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from accounts.models import Role, Team 
from django.contrib.auth import get_user_model


class IssueDetailView(LoginRequiredMixin,DetailView):
    template_name  = "issues/detail.html"
    model = Issue
    
class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]
    
    def form_valid(self,form):
        form.instance.reporter = self.request.user
        return super ().form_valid(form)
    
    def test_func(self):
        role = Role.objects.get(name="product owner")
        return self.user.role == role 
    

class IssueUpdateView(LoginRequiredMixin, UpdateView):
    template_name ="issues/edit.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]

    def form_valid(self, form):
        issue = self.get_object()
        role = Role.objects.get(name="scrum master")
        if (form.instance.assignee != issue.assignee
            and role != self.request.user.role):
            form.instance.assignee = issue.assignee
        return super().form_valid(form)

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

class IssueListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    template_name = "issues/new.html"
    model = Issue 
    fields = ["summary", "description","assignee", "status"]

    def test_func(self):
        role = Role.objects.get(name="product owner")
        return role == self.request.user.role

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_team = self.request.user.team
        po_role = Role.objects.get(name="product owner")
        product_owner = get_user_model;().objects.get(
            role=po_role, team =user_team)
        context["issue_list"] = Issue.objects.filter(
            reporter=product_owner
        ).order_by("created_on").reverse()
        return context