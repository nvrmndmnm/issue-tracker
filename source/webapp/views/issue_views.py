from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View, FormView, ListView, DetailView, CreateView
from webapp.models import Issue
from webapp.forms import IssueForm, SearchForm, ProjectIssueForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


class SearchView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issue/index.html'
    ordering = ['-time_created']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'q': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset

    def get_query(self):
        query = Q(summary__icontains=self.search_value)
        return query

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['q']


class IndexView(SearchView):
    def get(self, request, *args, **kwargs):
        self.filtered_value = self.get_filtered_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filtered_value:
            queryset = queryset.filter(status_id=self.filtered_value)
        return queryset

    def get_filtered_value(self):
        if self.request.GET.get('status'):
            return self.request.GET.get('status')

    def get_query(self):
        # Class method is overridden so that searching from header is global and provides results by summary,
        # while searching from the issues list provides results by description as well
        query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
        return query


class IssueView(UserPassesTestMixin, DetailView):
    template_name = 'issue/issue.html'
    context_object_name = 'issue'
    model = Issue

    permission_required = 'webapp.superuser', 'webapp.change_issue'

    def test_func(self):
        return self.request.user in self.get_issue().project.users.all() or \
               self.request.user.has_perm(self.permission_required)

    def get_issue(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)


class CreateIssueView(PermissionRequiredMixin, CreateView):
    model = Issue
    template_name = 'issue/create.html'
    form_class = IssueForm
    permission_required = ['webapp.superuser']

    def get_success_url(self):
        return reverse('webapp:issue', kwargs={'pk': self.object.pk})


class EditIssueView(UserPassesTestMixin, FormView):
    template_name = 'issue/update.html'
    form_class = ProjectIssueForm
    permission_required = 'webapp.superuser', 'webapp.change_issue'

    def test_func(self):
        return self.request.user in self.get_object().project.users.all() or \
               self.request.user.has_perm(self.permission_required)

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
        return reverse('webapp:issue', kwargs={'pk': self.issue.pk})


class DeleteIssueView(UserPassesTestMixin, View):
    template_name = 'issue/delete.html'
    permission_required = 'webapp.superuser'

    def test_func(self):
        return self.request.user in self.get_object().project.users.all() or \
               self.request.user.has_perm(self.permission_required)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        context = {"issue": issue}
        return render(request, "issue/delete.html", context)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect(request.META.get('HTTP_REFERER', 'index'))
