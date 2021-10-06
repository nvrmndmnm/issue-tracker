from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View, FormView, ListView, DetailView
from webapp.models import Issue
from webapp.forms import IssueForm, SearchForm


class SearchView(ListView):
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
        # Для примера тут используется только одно условие поискового запроса,
        # которое переопределяется в другом представлении
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
        if self.kwargs.get('status_pk'):
            return self.kwargs['status_pk']

    def get_query(self):
        # Метод класса переопределён, поэтому поиск в хэдере глобальный и ищет только по summary,
        # а поиск в списке задач отфильтрован и ищет ещё по description
        query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
        return query


class IssueView(DetailView):
    template_name = 'issue/issue.html'
    context_object_name = 'issue'
    model = Issue


class AddIssueView(FormView):
    template_name = 'issue/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue', kwargs={'pk': self.issue.pk})


class EditIssueView(FormView):
    template_name = 'issue/update.html'
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
        return render(request, "issue/delete.html", context)

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
