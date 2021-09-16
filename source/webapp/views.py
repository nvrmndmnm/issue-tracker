from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Issue


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs["issues"] = Issue.objects.all()
        return super().get_context_data(**kwargs)


class IssueView(TemplateView):
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        kwargs["issue"] = get_object_or_404(Issue, pk=kwargs["pk"])
        return super().get_context_data(**kwargs)


class AddIssueView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        context = {"issues": issues}
        return render(request, "add_issue.html", context)


class EditIssueView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        context = {"issues": issues}
        return render(request, "edit_issue.html", context)


class DeleteIssueView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        context = {"issues": issues}
        return render(request, "delete_issue.html", context)
