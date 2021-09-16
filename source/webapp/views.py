from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Issue
from webapp.forms import IssueForm


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
        form = IssueForm()
        context = {"form": form}
        return render(request, "add_issue.html", context)

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        context = {"form": form}
        if form.is_valid():
            issue = Issue.objects.create(**form.cleaned_data)
            return redirect('issue', pk=issue.pk)
        else:
            return render(request, "add_issue.html", context)


class EditIssueView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        form = IssueForm(initial={
            'summary': issue.summary,
            'type': issue.type,
            'status': issue.status,
            'description': issue.description
        })
        context = {"form": form, "issue": issue}
        return render(request, "edit_issue.html", context)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        form = IssueForm(data=request.POST)
        context = {"form": form}
        if form.is_valid():
            issue.summary = form.cleaned_data['summary']
            issue.type = form.cleaned_data['type']
            issue.status = form.cleaned_data['status']
            issue.description = form.cleaned_data['description']
            issue.save()
        else:
            return render(request, "edit_issue.html", context)
        return redirect('issue', pk=issue.pk)


class DeleteIssueView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        context = {"issue": issue}
        return render(request, "delete_issue.html", context)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
