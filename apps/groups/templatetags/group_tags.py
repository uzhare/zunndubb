from django import template

register = template.Library()


@register.inclusion_tag('groups/group_users.html', takes_context=True)
def group_users(context, group):
    context.update({'group_users': group.group_users.all()})
    return context

@register.filter
def get_is_admin(group, user):
	return group.is_admin(user)

@register.filter
def get_is_member(group, user):
	return group.is_member(user)