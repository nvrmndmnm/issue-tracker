from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView, ListView
from webapp.models import Issue
from webapp.forms import IssueForm


class IndexView(ListView):
    model = Issue
    template_name = 'index.html'
    ordering = ['-time_created']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.filtered_value = self.get_filtered_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filtered_value:
            queryset = queryset.filter(status_id=self.filtered_value)
        return queryset

    def get_filtered_value(self):
        if self.kwargs.get('status_pk'):
            return self.kwargs['status_pk']


class IssueView(TemplateView):
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        kwargs["issue"] = get_object_or_404(Issue, pk=kwargs["pk"])
        return super().get_context_data(**kwargs)


class AddIssueView(FormView):
    template_name = 'add_issue.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue', kwargs={'pk': self.issue.pk})


class EditIssueView(FormView):
    template_name = 'edit_issue.html'
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue', kwargs={'pk': self.issue.pk})


class DeleteIssueView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        context = {"issue": issue}
        return render(request, "delete_issue.html", context)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
