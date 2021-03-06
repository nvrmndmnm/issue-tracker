from django.core.validators import BaseValidator, RegexValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth import get_user_model


@deconstructible
class MinValueValidator(BaseValidator):
    message = 'Value "%(value)s" is %(show_value)d symbols long, while it should be at least %(limit_value)d symbols.'

    def clean(self, x):
        return len(x)

    def compare(self, a, b):
        return a < b


class Issue(models.Model):
    summary = models.CharField(max_length=150, verbose_name='Summary',
                               validators=[MinValueValidator(5),
                                           RegexValidator(regex='^[ a-zA-Z0-9]*$',
                                                          message='Value should only contain Latin letters and numbers.'
                                                          )])
    description = models.TextField(max_length=2000, verbose_name='Description')
    status = models.ForeignKey('webapp.IssueStatus', on_delete=models.RESTRICT,
                               default='webapp.IssueStatus', verbose_name='Status', related_name='statuses')
    types = models.ManyToManyField('webapp.IssueType', verbose_name='Types',
                                   related_name='types')
    project = models.ForeignKey('webapp.Project', on_delete=models.RESTRICT, related_name='project',
                                default=1, verbose_name='Issue project')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.summary}"

    class Meta:
        permissions = [
            ('superuser', 'All operations available')
        ]


class IssueType(models.Model):
    name = models.CharField(max_length=30, verbose_name='Type')

    def __str__(self):
        return f"{self.name}"


class IssueStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name='Status')

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    date_started = models.DateField(verbose_name='Start date')
    date_ended = models.DateField(verbose_name='End date', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='Project name',
                            validators=[MinValueValidator(5),
                                        RegexValidator(regex='^[ a-zA-Z0-9]*$',
                                                       message='Value should only contain Latin letters and numbers.'
                                                       )])
    users = models.ManyToManyField(get_user_model(), verbose_name='Users', related_name='users')
    description = models.TextField(max_length=2000, verbose_name='Project description')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        permissions = [
            ('superuser', 'All operations available')
        ]
