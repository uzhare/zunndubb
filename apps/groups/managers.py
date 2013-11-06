from django.db import models


class GroupManager(models.Manager):

    def get_for_user(self, user):
        return self.get_query_set().filter(users=user)


class ActiveGroupManager(GroupManager):
    """
    A more useful extension of the default manager which returns querysets
    including only active groups
    """

    def get_query_set(self):
        return super(ActiveGroupManager,
                self).get_query_set().filter(is_active=True)