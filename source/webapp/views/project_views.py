from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from webapp.forms import ProjectIssueForm, ProjectUsersForm
from webapp.views.issue_views import IndexView
from webapp.models import Project, Issue


class ProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/list.html'
    ordering = ['id']
    paginate_by = 10


class ProjectView(IndexView, FormView):
    form_class = ProjectUsersForm

    def get(self, request, *args, **kwargs):
        self.project_id = self.get_project_id()
        self.project = self.get_project()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['project_pk'] = self.project_id
        context['project'] = self.project
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(project=self.project_id)
        return queryset

    def get_project_id(self):
        if self.kwargs.get('project_pk'):
            return self.kwargs['project_pk']

    def get_project(self):
        return get_object_or_404(Project, pk=self.project_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.project
        return kwargs


class CreateProjectIssueView(UserPassesTestMixin, CreateView):
    model = Issue
    form_class = ProjectIssueForm
    template_name = 'issue/create.html'
    permission_required = ['webapp.add_issue', 'webapp.superuser']

    def test_func(self):
        return self.request.user in self.get_project().users.all() or\
               self.request.user.has_perm(self.permission_required)

    def form_valid(self, form):
        pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=pk)
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        form.save_m2m()
        return redirect('webapp:issue', pk=issue.pk)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['project_pk'] = self.get_project().pk
        return context

    def get_project(self):
        if self.kwargs.get('project_pk'):
            return get_object_or_404(Project, pk=self.kwargs['project_pk'])


class CreateProjectView(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'date_started', 'date_ended', 'description']
    template_name = 'project/create.html'
    permission_required = ['webapp.add_project', 'webapp.superuser']

    def form_valid(self, form):
        form.save()
        form.instance.users.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:projects')


class UpdateProjectUsersView(UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectUsersForm
    template_name = 'project/users.html'
    permission_required = ['webapp.change_project', 'webapp.superuser']

    def test_func(self):
        return self.request.user in self.get_object().users.all() or\
               self.request.user.has_perm(self.permission_required)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('project_pk')
        return get_object_or_404(Project, pk=pk)

    def form_valid(self, form):
        self.project = form.save()
        if self.request.user not in self.project.users.all():
            self.project.users.add(self.request.user)
            form.add_error('users', 'Cannot remove yourself.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'project_pk': self.project.pk})
