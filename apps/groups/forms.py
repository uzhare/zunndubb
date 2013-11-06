from django import forms
from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _

from .models import Group, GroupUser, get_user_model
from .utils import create_group
from apps.profiles.models import Profile


class GroupForm(forms.ModelForm):
    """Form class for updating Groups"""
    owner = forms.ModelChoiceField(GroupUser.objects.all())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = self.instance.group_users.filter(
                is_admin=True, user__is_active=True)
        self.fields['owner'].initial = self.instance.owner.group_user

    class Meta:
        model = Group
        exclude = ('users', 'is_active')

    def save(self, commit=True):
        if self.instance.owner.group_user != self.cleaned_data['owner']:
            self.instance.owner.group_user = self.cleaned_data['owner']
            self.instance.owner.save()
        return super(GroupForm, self).save(commit=commit)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        if owner != self.instance.owner.group_user:
            if self.request.user != self.instance.owner.group_user.user:
                raise forms.ValidationError(_("Only the group owner can change ownerhip"))
        return owner


class GroupUserAddForm(forms.ModelForm):
    """Form class for adding GroupUsers to an existing Group"""
    email = forms.EmailField(max_length=75)

    def __init__(self, request, group, *args, **kwargs):
        self.request = request
        self.group = group
        super(GroupUserAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GroupUser
        exclude = ('user', 'group')

    def save(self, *args, **kwargs):
        """
        The save method should create a new GroupUser linking the User
        matching the provided email address.

        """
        try:
            user = get_user_model().objects.get(email__iexact=self.cleaned_data['email'])
        except get_user_model().DoesNotExist:
            raise forms.ValidationError(_("No member with this email address!"))
        return GroupUser.objects.create(user=user,
                group=self.group,
                is_admin=self.cleaned_data['is_admin'])

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.group.users.filter(email=email):
            raise forms.ValidationError(_("There is already an group member with this email address!"))
        return email

class GroupJoinForm(forms.ModelForm):
    """ Form class for joining a Group"""
    
    def __init__(self, request, group, *args, **kwargs):
        self.request = request
        self.group = group
        super(GroupJoinForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GroupUser
        exclude = ('user','group','is_admin')

    def save(self, *args, **kwargs):
        """ The save method creates a new GroupUser"""
        print "*"*80
        user = get_user_model().objects.get(username=self.request.user)
        # TODO: Check if user already a group member.
        return GroupUser.objects.create(user=user,
                group=self.group,
                is_admin=False)



class GroupUserForm(forms.ModelForm):
    """Form class for updating GroupUsers"""

    class Meta:
        model = GroupUser
        exclude = ('group', 'user')

    def clean_is_admin(self):
        is_admin = self.cleaned_data['is_admin']
        if self.instance.group.owner.group_user == self.instance and not is_admin:
            raise forms.ValidationError(_("The group owner must be an admin"))
        return is_admin


class GroupAddForm(forms.ModelForm):
    """
    Form class for creating a new group, complete with new owner, including a
    User instance, GroupUser instance, and GroupOwner instance.
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GroupAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Group
        exclude = ('users', 'is_active')

    def save(self, **kwargs):
        """
        Create the group, then get the user, then make the owner.
        """
        is_active = True

        user = Profile.objects.get(username=self.request.user)

        return create_group(user, self.cleaned_data['name'],
                self.cleaned_data['slug'], is_active=is_active)