from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class VerifyTokenRequest(BaseModel):
    token: str


class RefreshTokenRequest(BaseModel):
    refresh: str


class TokenResponse(BaseModel):
    refresh_token: str
    access_token: str
