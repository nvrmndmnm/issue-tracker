from django.contrib import admin
from webapp.models import Issue, IssueType, IssueStatus


class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "summary", "time_created"]
    list_filter = ["id"]
    search_fields = ["summary"]
    fields = ["summary", "description", "time_created"]
    readonly_fields = ["time_created"]


admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueType)
admin.site.register(IssueStatus)
