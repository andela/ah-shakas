# authors/apps/notifications.py
# Model for the Notification

from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import ArticlesModel
from django.utils.timezone import now


class UserNotifications(models.Model):
    """ Notification model """
    author = models.ForeignKey(ArticlesModel, related_name="+", on_delete = models.CASCADE, blank=True)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete = models.CASCADE, blank=True)
    article = models.ForeignKey(ArticlesModel, on_delete = models.CASCADE, blank=True)
    notification = models.TextField()
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Notice " - " : will order by created most recently
        ordering = ('-created_at',)

    def __str__(self):
        "return the notification"
        return "{}".format(self.notification)