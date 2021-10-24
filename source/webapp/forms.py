from django import forms
from webapp.models import Issue, IssueType, Project
from django.contrib.auth import get_user_model


class IssueForm(forms.ModelForm):
    types = forms.ModelMultipleChoiceField(queryset=IssueType.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True,
                                           initial=IssueType.objects.first(),
                                           label="Type")

    class Meta:
        model = Issue
        fields = ["summary", "project", "types", "status", "description"]


class ProjectIssueForm(IssueForm):
    class Meta:
        model = Issue
        fields = ["summary", "types", "status", "description"]


class ProjectUsersForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True,
                                           initial=get_user_model().objects.first(),
                                           label="Users")

    class Meta:
        model = Project
        fields = ["users"]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Search')
