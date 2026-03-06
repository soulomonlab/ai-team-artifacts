import pytest
from output.code.permissions import Role, role_at_least, has_permission


class DummyResource:
    def __init__(self, owner_id=None, permissions=None):
        self.owner_id = owner_id
        self.permissions = permissions or {}


def test_role_hierarchy():
    assert role_at_least(Role.OWNER, Role.WRITE)
    assert role_at_least(Role.WRITE, Role.READ)
    assert not role_at_least(Role.READ, Role.WRITE)


def test_has_permission_owner():
    r = DummyResource(owner_id=10, permissions={})
    assert has_permission(10, r, Role.OWNER)
    assert has_permission(10, r, Role.WRITE)
    assert has_permission(10, r, Role.READ)


def test_has_permission_explicit_write():
    r = DummyResource(owner_id=1, permissions={20: Role.WRITE})
    assert has_permission(20, r, Role.READ)
    assert has_permission(20, r, Role.WRITE)
    assert not has_permission(20, r, Role.OWNER)


def test_has_permission_missing():
    r = DummyResource(owner_id=1, permissions={})
    assert not has_permission(30, r, Role.READ)


def test_has_permission_string_role():
    r = DummyResource(owner_id=1, permissions={40: "read"})
    assert has_permission(40, r, Role.READ)
