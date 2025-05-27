from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
implantation_scheme = HTTPBearer()


@router.get("/mobile/tree")
def get_tree_by_id(
    id: str = Query(..., alias="site", description="Site id"),
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return {"MobileTree": "Placeholder"}


@router.get("/mobile/info")
def get_asset_info_by_id(
    id: str = Query(..., alias="site", description="Site id"),
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return {"MobileInfo": "Placeholder"}


@router.get("/mobile/static")
def get_static_asset(
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials

    return {"MobileStatic": "Placeholder"}


@router.get("/mobile/static/get_lubricants")
def get_lubricants(
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return {"MobileStaticGetLubricants": "Placeholder"}
