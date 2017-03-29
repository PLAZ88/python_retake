from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User

# Create your models here.

class FriendManager(models.Manager):
    def process(self, id):

        user = User.objects.get(id=id)
        friend = self.create(friend_name=user, friend_id=user)
        friend.relationships.add(user)

        return {'friend': friend}


class Friend(models.Model):
    friend_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friend_id = models.ForeignKey(User, related_name = "friends", blank=True, null=True)
    relationships = models.ManyToManyField(User, related_name="relationships")
    objects = FriendManager()
