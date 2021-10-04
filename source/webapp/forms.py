from django import forms
from webapp.models import Issue, IssueType


class IssueForm(forms.ModelForm):
    types = forms.ModelMultipleChoiceField(queryset=IssueType.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True,
                                           initial=IssueType.objects.first(),
                                           label="Type")

    class Meta:
        model = Issue
        fields = ["summary", "types", "status", "description"]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Search')
