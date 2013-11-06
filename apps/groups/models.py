from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import permalink, get_model
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from .managers import GroupManager, ActiveGroupManager


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def get_user_model():
    """
    Returns the chosen user model as a class. 

    """
    try:
        klass = get_model(USER_MODEL.split('.')[0], USER_MODEL.split('.')[1])
    except:
        raise ImproperlyConfigured("Your user class, {0}, is improperly defined".format(klass_string))
    return klass


class Group(models.Model):
    """
    The umbrella object with which users can be associated.

    An Group can have multiple users but only one who can be designated
    the owner user.

    """
    name = models.CharField(max_length=256,
            help_text=_("The name of the group"))
    slug = models.SlugField(max_length=256, blank=False, unique=True,
            help_text=_("The name in all lowercase, suitable for URL identification"))
    users = models.ManyToManyField(USER_MODEL, through="GroupUser")
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)

    objects = GroupManager()
    active = ActiveGroupManager()

    class Meta:
        ordering = ['name']
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('group_detail', (), {'group_pk': self.pk})

    def add_user(self, user, is_admin=False):
        """
        Adds a new user and if the first user makes the user an admin and
        the owner.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True
        group_user = GroupUser.objects.create(user=user,
                group=self, is_admin=is_admin)
        if users_count == 0:
            GroupOwner.objects.create(group=self,
                    group_user=group_user)
        return group_user

    def get_or_add_user(self, user, is_admin=False):
        """
        Adds a new user to the group, and if it's the first user makes
        the user an admin and the owner. Uses the `get_or_create` method to
        create or return the existing user.

        `user` should be a user instance, e.g. `auth.User`.

        Returns the same tuple as the `get_or_create` method, the
        `GroupUser` and a boolean value indicating whether the
        GroupUser was created or not.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True

        group_user, created = GroupUser.objects.get_or_create(
                group=self, user=user, defaults={'is_admin': is_admin})

        if users_count == 0:
            GroupOwner.objects.create(group=self,
                    group_user=group_user)

        return group_user, created

    def is_member(self, user):
        return True if user in self.users.all() else False

    def is_admin(self, user):
        return True if self.group_users.filter(user=user, is_admin=True) else False


class GroupUser(models.Model):
    """
    ManyToMany through field relating Users to Groups.

    It is possible for a User to be a member of multiple groups, so this
    class relates the GroupUser to the User model using a ForeignKey
    relationship, rather than a OneToOne relationship.

    """
    user = models.ForeignKey(USER_MODEL, related_name="group_users")
    group = models.ForeignKey(Group,
            related_name="group_users")
    is_admin = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['group', 'user']
        unique_together = ('user', 'group')
        verbose_name = _("group user")
        verbose_name_plural = _("group users")

    def __str__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active else
                self.user.email, self.group.name)

    def delete(self, using=None):
        """
        If the group user is also the owner, this should not be deleted
        unless it's part of a cascade from the Group.

        If there is no owner then the deletion should proceed.
        """
        from .exceptions import OwnershipRequired
        try:
            if self.group.owner.group_user.id == self.id:
                raise OwnershipRequired(_("Cannot delete group owner before group or transferring group."))
        except GroupOwner.DoesNotExist:
            pass
        super(GroupUser, self).delete(using=using)

    @permalink
    def get_absolute_url(self):
        return ('group_user_detail', (),
                {'group_pk': self.group.pk, 'user_pk': self.user.pk})

    @property
    def name(self):
        if hasattr(self.user, 'get_full_name'):
            return self.user.get_full_name()
        return "{0}".format(self.user)


class GroupOwner(models.Model):
    """Each group must have one and only one group owner."""

    group = models.OneToOneField(Group, related_name="owner")
    group_user = models.OneToOneField(GroupUser,
            related_name="owner_group")

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("group owner")
        verbose_name_plural = _("group owners")

    def __str__(self):
        return u"{0}: {1}".format(self.group, self.group_user)

    def save(self, *args, **kwargs):
        """
        Extends the default save method by verifying that the chosen
        group user is associated with the group.

        """
        from .exceptions import GroupMismatch
        if self.group_user.group != self.group:
            raise GroupMismatch
        else:
            super(GroupOwner, self).save(*args, **kwargs)
