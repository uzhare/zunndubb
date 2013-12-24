from .models import Group


def get_user_groups(request):
	print "Context_processor"
	user_groups = Group.active.filter(users=request.user)

	return {
			'my_groups': user_groups,
		}