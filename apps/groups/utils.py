from .models import (Group, GroupUser,
                    GroupOwner)


def create_group(user, name, description, slug, is_active=True):
    """
    Returns a new group, also creating an initial group user who
    is the owner.
    """
    group = Group.objects.create(name=name, description=description,
            slug=slug, is_active=is_active)
    new_user = GroupUser.objects.create(group=group,
            user=user, is_admin=True)
    GroupOwner.objects.create(group=group,
            group_user=new_user)
    return group


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)
