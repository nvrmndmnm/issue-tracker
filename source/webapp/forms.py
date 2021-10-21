from django import forms
from webapp.models import Issue, IssueType, Project, User


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
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True,
                                           initial=User.objects.first(),
                                           label="Users")

    class Meta:
        model = Project
        fields = ["users"]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Search')
