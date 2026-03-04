from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

@router.post("/auth/login", response_model=AuthResponse)
def login(req: LoginRequest):
    # skeleton: validate credentials -> issue JWT (stubbed)
    if req.email == "alice@example.com" and req.password == "securePass123":
        return AuthResponse(access_token="<jwt>", expires_in=3600)
    raise HTTPException(status_code=401, detail="Invalid credentials")
