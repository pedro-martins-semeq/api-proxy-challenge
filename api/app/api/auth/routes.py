from fastapi import APIRouter


router = APIRouter()


@router.post("/login")
def login(data):
    return {"Login": "Placeholder"}


@router.post("/token/verify")
def verify_token(data):
    return {"TokenVerify": "Placeholder"}


@router.post("/token/refresh")
def refresh_token(data):
    return {"TokenRefresh": "Placeholder"}
