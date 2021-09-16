from django.db import models


class Issue(models.Model):
    summary = models.CharField(max_length=150, verbose_name='Summary')
    description = models.CharField(max_length=2000, verbose_name='Description')
    status = models.ForeignKey('webapp.IssueStatus', on_delete=models.RESTRICT,
                               verbose_name='Status', related_name='statuses')
    type = models.ForeignKey('webapp.IssueType', on_delete=models.RESTRICT,
                             verbose_name='Type', related_name='types')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.summary}"


class IssueType(models.Model):
    name = models.CharField(max_length=30, verbose_name='Type')


class IssueStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name='Status')
