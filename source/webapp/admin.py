from django.contrib import admin
from webapp.models import Issue, IssueType, IssueStatus, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "project", "summary", "status", "time_created"]
    list_filter = ["status", "types"]
    search_fields = ["summary"]
    fields = ["summary", "project", "description", "status", "types", "time_created"]
    readonly_fields = ["time_created"]


admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueType)
admin.site.register(IssueStatus)
admin.site.register(Project)
