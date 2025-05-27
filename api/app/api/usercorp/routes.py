from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.api.usercorp.service import UsercorpService

router = APIRouter()
usercorp_service = UsercorpService()
usercorp_scheme = HTTPBearer()


@router.get("/")
def retrieve_usercorp_data(
    credentials: HTTPAuthorizationCredentials = Depends(usercorp_scheme),
):
    token = credentials.credentials
    return usercorp_service.retrieve_usercorp_data(token)
