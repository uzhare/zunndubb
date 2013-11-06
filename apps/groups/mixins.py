from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Group, GroupUser


class GroupMixin(object):
    """Mixin used like a SingleObjectMixin to fetch an group"""

    group_model = Group
    group_context_name = 'group'

    def get_group_model(self):
        return self.group_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.group_context_name: self.get_group()})
        return super(GroupMixin, self).get_context_data(**kwargs)

    def get_object(self):
        if hasattr(self, 'group'):
            return self.group
        group_pk = self.kwargs.get('group_pk', None)
        self.group = get_object_or_404(self.get_group_model(), pk=group_pk)
        return self.group
    get_group = get_object # Now available when `get_object` is overridden


class GroupUserMixin(GroupMixin):
    """Mixin used like a SingleObjectMixin to fetch an group user"""

    user_model = GroupUser
    group_user_context_name = 'group_user'

    def get_user_model(self):
        return self.user_model

    def get_context_data(self, **kwargs):
        kwargs = super(GroupUserMixin, self).get_context_data(**kwargs)
        kwargs.update({self.group_user_context_name: self.object,
            self.group_context_name: self.object.group})
        return kwargs

    def get_object(self):
        """ Returns the GroupUser object based on the primary keys for both
        the group and the group user.
        """
        if hasattr(self, 'group_user'):
            return self.group_user
        group_pk = self.kwargs.get('group_pk', None)
        user_pk = self.kwargs.get('user_pk', None)
        self.group_user = get_object_or_404(
                GroupUser.objects.select_related(),
                user__pk=user_pk, group__pk=group_pk)
        return self.group_user


class MembershipRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.group = self.get_group()
        if not self.group.is_member(request.user) and not \
                    request.user.is_superuser:
            return HttpResponseForbidden(_("Wrong group"))
        return super(MembershipRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class AdminRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.group = self.get_group()
        if not self.group.is_admin(request.user) and not \
                    request.user.is_superuser:
            return HttpResponseForbidden(_("Sorry, admins only"))
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class OwnerRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.group = self.get_group()
        if self.group.owner.group_user.user != request.user \
                    and not request.user.is_superuser:
            return HttpResponseForbidden(_("You are not the group owner"))
        return super(OwnerRequiredMixin, self).dispatch(request, *args,
                **kwargs)
