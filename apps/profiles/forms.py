from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from .models import Profile
from django.db.models import Q


class UserEmailForm(forms.Form):
    error_messages = {
        'duplicate_email': _("A user with that email already exists.")
    }
    email = forms.EmailField(label=_("Email"), max_length=256)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class UserSettingForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'duplicate_username': _("A user with same username already exists.")
    }
    user = forms.CharField(max_length=128, required=False)
    
    class Meta:
        model = Profile
        fields = ('username', 'name', 'email', 'avatar')
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserSettingForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = self.user
        try:
            Profile.objects.get(Q(username=username), ~Q(username=user))
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = self.user
        try:
            Profile.objects.get(Q(email=email), ~Q(username=user))
        except Profile.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        return avatar