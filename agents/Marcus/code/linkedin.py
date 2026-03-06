from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import httpx
import os
from datetime import datetime, timedelta

from ..models.linkedin_token import LinkedInToken, Base
from ..database import get_db
from ..encryption import encrypt, decrypt

router = APIRouter(prefix="/api/v1/oauth/linkedin", tags=["oauth"])

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


@router.post("/connect")
async def connect(code: str, db: Session = Depends(get_db), request: Request = None, user=Depends(None)):
    # user dependency placeholder - integrate with auth system
    user_id = getattr(user, "id", 1)
    if not CLIENT_ID or not CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="LinkedIn client not configured")

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        resp = await client.post(TOKEN_URL, data=data)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code with LinkedIn")
        payload = resp.json()

    access_token = payload.get("access_token")
    expires_in = payload.get("expires_in")
    # LinkedIn may not return refresh token in all apps
    refresh_token = payload.get("refresh_token")

    expires_at = None
    if expires_in:
        expires_at = datetime.utcnow() + timedelta(seconds=int(expires_in))

    enc_access = encrypt(access_token)
    enc_refresh = encrypt(refresh_token) if refresh_token else None

    token = LinkedInToken(
        user_id=user_id,
        access_token=enc_access.decode() if enc_access else None,
        refresh_token=enc_refresh.decode() if enc_refresh else None,
        expires_at=expires_at,
        scopes=None,
    )
    db.add(token)
    db.commit()
    db.refresh(token)

    return {"status": "connected", "id": token.id}


@router.post("/disconnect")
async def disconnect(db: Session = Depends(get_db), user=Depends(None)):
    user_id = getattr(user, "id", 1)
    token = db.query(LinkedInToken).filter_by(user_id=user_id, revoked=False).first()
    if not token:
        raise HTTPException(status_code=404, detail="No linked LinkedIn token")
    token.revoked = True
    db.add(token)
    db.commit()
    return {"status": "disconnected"}


async def refresh_token_if_needed(db: Session, token: LinkedInToken):
    if not token.refresh_token:
        return token
    if token.expires_at and token.expires_at > datetime.utcnow() + timedelta(minutes=2):
        return token

    dec_refresh = decrypt(token.refresh_token.encode())
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": dec_refresh,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        resp = await client.post(TOKEN_URL, data=data)
        if resp.status_code != 200:
            # mark revoked if refresh failed
            token.revoked = True
            db.add(token)
            db.commit()
            return token
        payload = resp.json()

    access_token = payload.get("access_token")
    expires_in = payload.get("expires_in")
    refresh_token = payload.get("refresh_token")

    token.access_token = encrypt(access_token).decode() if access_token else token.access_token
    token.refresh_token = encrypt(refresh_token).decode() if refresh_token else token.refresh_token
    token.expires_at = datetime.utcnow() + timedelta(seconds=int(expires_in)) if expires_in else token.expires_at
    db.add(token)
    db.commit()
    db.refresh(token)
    return token
