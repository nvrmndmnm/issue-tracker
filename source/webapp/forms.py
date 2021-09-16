from django import forms
from django.forms import widgets
from webapp.models import IssueType, IssueStatus


class IssueForm(forms.Form):
    summary = forms.CharField(max_length=150,
                              required=True,
                              label="Summary")
    type = forms.ModelChoiceField(queryset=IssueType.objects.all(),
                                  required=True,
                                  initial=IssueType.objects.first(),
                                  label="Type")
    status = forms.ModelChoiceField(queryset=IssueStatus.objects.all(),
                                    required=True,
                                    initial=IssueStatus.objects.first(),
                                    label="Status")
    description = forms.CharField(widget=widgets.Textarea,
                                  required=True,
                                  max_length=2000,
                                  label="Description")
