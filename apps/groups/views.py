from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
        DeleteView, FormView)

from .models import *
from .mixins import (GroupMixin, GroupUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)
from .forms import (GroupForm, GroupUserForm, GroupAddForm,
                    GroupUserAddForm, GroupJoinForm)
from .utils import create_group


class AllGroupListView(ListView):
    model = Group
    template_name = 'groups/all_groups.html'
    context_object_name = "groups"


class GroupListView(ListView):
    queryset = Group.active.all()
    context_object_name = "groups"

    def get_queryset(self):
        return super(GroupListView,
                self).get_queryset().filter(users=self.request.user)


class GroupDetailView(GroupMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['group_users'] = self.group.group_users.all()
        context['group'] = self.group
        return context


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupAddForm
    template_name = 'groups/group_form.html'

    def get_success_url(self):
        return reverse("group_list")

    def get_form_kwargs(self):
        kwargs = super(GroupCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class GroupUpdateView(GroupMixin, UpdateView):
    form_class = GroupForm

    def get_form_kwargs(self):
        kwargs = super(GroupUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class GroupDeleteView(GroupMixin, DeleteView):
    def get_success_url(self):
        return reverse("group_list")


class GroupUserListView(GroupMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.group = self.get_group()
        self.object_list = self.group.group_users.all()
        context = self.get_context_data(object_list=self.object_list,
                group_users=self.object_list,
                group=self.group)
        return self.render_to_response(context)


class GroupUserDetailView(GroupUserMixin, DetailView):
    pass


class GroupJoinView(GroupMixin, CreateView):
    form_class = GroupJoinForm
    template_name = 'groups/group_join.html'

    def get_success_url(self):
        return reverse('group_list_all')

    def get_form_kwargs(self):
        kwargs = super(GroupJoinView, self).get_form_kwargs()
        kwargs.update({'group': self.group,
            'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.group = self.get_object()
        return super(GroupJoinView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.group = self.get_object()
        return super(GroupJoinView, self).post(request, *args, **kwargs)


class GroupUserCreateView(GroupMixin, CreateView):
    form_class = GroupUserAddForm
    template_name = 'groups/groupuser_form.html'

    def get_success_url(self):
        return reverse('group_user_list',
                kwargs={'group_pk': self.object.group.pk})

    def get_form_kwargs(self):
        kwargs = super(GroupUserCreateView, self).get_form_kwargs()
        kwargs.update({'group': self.group,
            'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.group = self.get_object()
        return super(GroupUserCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.group = self.get_object()
        return super(GroupUserCreateView, self).post(request, *args, **kwargs)


class GroupUserUpdateView(GroupUserMixin, UpdateView):
    form_class = GroupUserForm


class GroupUserDeleteView(GroupUserMixin, DeleteView):
    def get_success_url(self):
        return reverse('group_user_list',
                kwargs={'group_pk': self.object.group.pk})

