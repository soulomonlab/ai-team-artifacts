from enum import Enum
from typing import Optional


class Role(str, Enum):
    OWNER = "owner"
    WRITE = "write"
    READ = "read"


# Simple permission hierarchy to compare roles
_ROLE_HIERARCHY = {
    Role.OWNER: 3,
    Role.WRITE: 2,
    Role.READ: 1,
}


def role_at_least(user_role: Role, required: Role) -> bool:
    """Return True if user_role >= required in permission hierarchy."""
    return _ROLE_HIERARCHY.get(user_role, 0) >= _ROLE_HIERARCHY.get(required, 0)


def has_permission(user_id: int, resource: "Resource", required: Role) -> bool:
    """Check whether user_id has at least `required` permission on resource.

    Resource is expected to expose a `permissions` mapping: {user_id: Role}
    This function intentionally keeps DB access out of scope and operates on the
    in-memory resource object to make it easy to unit test.
    """
    if resource is None:
        return False

    # Owners of the resource (resource.owner_id) implicitly have OWNER
    if hasattr(resource, "owner_id") and resource.owner_id == user_id:
        return True

    # Resource-level permissions mapping expected
    perms = getattr(resource, "permissions", None)
    if not isinstance(perms, dict):
        return False

    user_role = perms.get(user_id)
    if user_role is None:
        return False

    # If stored as string, normalize
    if isinstance(user_role, str):
        try:
            user_role = Role(user_role)
        except ValueError:
            return False

    return role_at_least(user_role, required)
