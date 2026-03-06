from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict

# Simplified in-memory data store for demo purposes. In production this should
# be replaced with DB models and proper transactional operations.
_FAKE_DB = {
    "resources": {},  # resource_id -> {owner_id: int, permissions: {user_id: role}}
    "users": {},
}

from ...permissions import Role, has_permission

router = APIRouter(prefix="/api/v1/sharing")


class InviteRequest(BaseModel):
    resource_id: int
    invitee_email: EmailStr
    role: Role


class ShareResponse(BaseModel):
    success: bool
    message: str


def get_user_id_from_token():
    # placeholder for auth dependency
    return 1


@router.post("/invite", response_model=ShareResponse)
def invite(req: InviteRequest, user_id: int = Depends(get_user_id_from_token)):
    resource = _FAKE_DB["resources"].get(req.resource_id)
    if resource is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    # only owners can invite
    if resource.get("owner_id") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can invite")

    # look up user by email
    invitee = next((u for u in _FAKE_DB["users"].values() if u["email"] == req.invitee_email), None)
    if invitee is None:
        # create pending invite; in production we'd send an email link to sign up
        _FAKE_DB.setdefault("pending_invites", []).append({
            "resource_id": req.resource_id,
            "email": req.invitee_email,
            "role": req.role,
        })
        return {"success": True, "message": "Invite created (pending user)"}

    # assign permission
    _FAKE_DB["resources"][req.resource_id]["permissions"][invitee["id"]] = req.role

    # In production: send email. Here we just return success
    return {"success": True, "message": "Invite sent"}


@router.post("/check", response_model=ShareResponse)
def check_permission(resource_id: int, required: Role, user_id: int = Depends(get_user_id_from_token)):
    resource = _FAKE_DB["resources"].get(resource_id)
    if resource is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    class DummyResource:
        def __init__(self, owner_id, permissions):
            self.owner_id = owner_id
            self.permissions = permissions

    res = DummyResource(owner_id=resource.get("owner_id"), permissions=resource.get("permissions", {}))

    allowed = has_permission(user_id, res, required)
    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return {"success": True, "message": "Allowed"}
