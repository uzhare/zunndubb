class OwnershipRequired(Exception):
    """
    Exception to raise if the owner is being removed before the
    group.
    """
    pass


class GroupMismatch(Exception):
    """
    Exception to raise if an group user from a different
    group is assigned to be an group's owner.
    """
    pass