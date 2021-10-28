from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.core.paginator import Paginator

from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordUpdateForm
from .models import Profile


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'list.html'
    ordering = ['pk']
    paginate_by = 10
    permission_required = 'auth.view_user'


class UserDetailView(UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0
    permission_required = 'auth.view_user'

    def get_context_data(self, **kwargs):
        projects = self.object.users.order_by('-id')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = projects
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user == self.get_object() or\
               self.request.user.has_perm(self.permission_required)


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileUpdateForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class UserPasswordUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'update_password.html'
    form_class = PasswordUpdateForm
    context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('accounts:login')
