from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        Group, Permission,
                                        _user_has_module_perms,
                                        _user_has_perm)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize, ResizeToFill, Adjust

from apps.wishlist.models import Wish

class ProfileManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The email must be provided')
        email = ProfileManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class Profile(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.CharField(_('email address'), max_length=256, unique=True)
    name = models.CharField(max_length=512, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    avatar_mini= ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(32, 32)], image_field='avatar',
            format='JPEG', options={'quality': 90})
    avatar_thumb = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(60, 80)], image_field='avatar',
            format='JPEG', options={'quality': 90})
    avatar_medium = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(120, 160)], image_field='avatar',
            format='JPEG', options={'quality': 90})
    avatar_large = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(160, 200)], image_field='avatar',
            format='JPEG', options={'quality': 90})
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'))
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text='Specific permissions for this user.')

    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profiles'

    def get_absolute_url(self):
        return "/~%s/" % (self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through his/her
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                if obj is not None:
                    permissions.update(backend.get_group_permissions(self,
                                                                     obj))
                else:
                    permissions.update(backend.get_group_permissions(self))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def downloading_list(self, number=None):
        if number:
            return Wish.in_progress.filter(profile=self)[:number]
        return Wish.in_progress.filter(profile=self)

    def want_list(self, number=None):
        if number:
            return Wish.want.filter(profile=self)[:number]
        return Wish.want.filter(profile=self)

    def has_list(self, number=None):
        if number:
            return Wish.have.filter(profile=self)[:number]
        return Wish.have.filter(profile=self)

    def is_downloading(self, movie):
        if movie.who_is_downloading.filter(profile=self).count() > 0:
            return True
        else:
            return False

    def has_it(self, movie):
        if movie.who_has.filter(profile=self).count() > 0:
            return True
        else:
            return False

    def wants_it(self, movie):
        if movie.who_wants.filter(profile=self).count() > 0:
            return True
        else:
            return False

    def doesnt_care(self, movie):
        if movie.who_doesnt_care.filter(profile=self).count() > 0:
            return True
        else:
            return False
