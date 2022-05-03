from webapp.models import Issue
from datetime import timedelta, datetime
from django.db.models import Q, F, Count
from calendar import monthrange

# Issues that were finished in the last month from the current date (by last update time)
Issue.objects.filter(Q(status__name__iexact='done') & Q(time_updated__gte=datetime.now() - timedelta(days=30)))

# Issues that have one of specified statuses AND one of specified types
Issue.objects.filter((Q(status__name__iexact='done') | Q(status__name__iexact='in progress')) &
                     (Q(types__name__iexact='bug') | Q(types__name__iexact='enhancement'))).distinct()

# Issues with "bug" (amy case) substring in the summary or with type "Bug", and with unfinished status
Issue.objects.filter((Q(summary__icontains='bug') | Q(types__name__iexact='bug')) &
                     ~Q(status__name__iexact='done')).distinct()

# List issues with following fields: id, summary, type name and status name
Issue.objects.values('id', 'summary', 'types__name', 'status__name')

# Issues with summary equal to description
Issue.objects.filter(summary__exact=F('description'))

# Number of issues of each type
Issue.objects.values('types__name').annotate(num_of_issues=Count('pk'))

# Auto define number of days in the current month
Issue.objects.filter(Q(status__name__iexact='done') & Q(time_updated__gte=datetime.now() - timedelta(
    days=monthrange(datetime.now().year, datetime.now().month)[1])))
