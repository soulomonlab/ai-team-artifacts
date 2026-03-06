from fastapi import APIRouter, Depends, Response, Cookie, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter(prefix="/auth", tags=["auth"])

# Schemas
class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

class UserOut(BaseModel):
    id: str
    email: EmailStr
    roles: List[str] = []

# In-memory stub - replace with real user service
fake_user = {"id": "u_123", "email": "kevin@example.com", "roles": ["user"]}

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, response: Response):
    if payload.email != fake_user["email"] or payload.password != "password":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")
    # set refresh token cookie
    response.set_cookie(
        "refresh_token",
        "fake_refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/api/v1/auth/refresh",
        max_age=7 * 24 * 3600,
    )
    return TokenOut(access_token="fake_access_token", expires_in=900)

@router.post("/refresh", response_model=TokenOut)
def refresh(response: Response, refresh_token: Optional[str] = Cookie(None)):
    if refresh_token != "fake_refresh_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_refresh")
    # rotate cookie
    response.set_cookie(
        "refresh_token",
        "fake_refresh_token_2",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/api/v1/auth/refresh",
        max_age=7 * 24 * 3600,
    )
    return TokenOut(access_token="fake_access_token_2", expires_in=900)

@router.post("/logout", status_code=204)
def logout(response: Response, refresh_token: Optional[str] = Cookie(None)):
    # Clear cookie
    response.delete_cookie("refresh_token", path="/api/v1/auth/refresh")
    return Response(status_code=204)

@router.post("/signup", status_code=201, response_model=TokenOut)
def signup(payload: LoginIn, response: Response):
    # pretend to create user
    response.set_cookie(
        "refresh_token",
        "fake_refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/api/v1/auth/refresh",
        max_age=7 * 24 * 3600,
    )
    return TokenOut(access_token="fake_access_token_signup", expires_in=900)

@router.get("/me", response_model=UserOut)
def me():
    return UserOut(**fake_user)
