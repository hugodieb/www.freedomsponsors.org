from core.models import *
from core.services.mail_services import *

__author__ = 'tony'


def find_issue_watches(issue):
    return Watch.objects.filter(entity='ISSUE', objid=issue.id)


def watch_issue(user, issue_id, reason):
    watch = _findIssueWatchOrNone(user, issue_id)
    if not watch:
        issue = Issue.objects.get(pk=issue_id)
        watch = Watch.newIssueWatch(issue, user, reason)
        watch.save()


def unwatch_issue(user, issue_id):
    watch = _findIssueWatchOrNone(user, issue_id)
    if watch:
        watch.delete()


def is_watching_issue(user, issue_id):
    watch = _findIssueWatchOrNone(user, issue_id)
    return not watch is None


def _findIssueWatchOrNone(user, issue_id):
    watches = Watch.objects.filter(user__id=user.id, entity='ISSUE', objid=issue_id)
    count = len(watches)
    if count > 1:
        notify_admin("WARNING: Database inconsistency", "more than one Watch for user %s / issue %s"%(user.id, issue_id))
    if count == 0:
        return None
    return watches[0]
