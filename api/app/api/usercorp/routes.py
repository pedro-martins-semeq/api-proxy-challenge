from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
usercorp_scheme = HTTPBearer()


@router.get("/")
def retrieve_usercorp_data(
    credentials: HTTPAuthorizationCredentials = Depends(usercorp_scheme),
):
    token = credentials.credentials
    return {"RetrieveUsercorp": "Placeholder"}
