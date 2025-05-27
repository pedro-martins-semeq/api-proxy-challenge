from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.implantation.service import ImplantationService

router = APIRouter()
implantation_service = ImplantationService()
implantation_scheme = HTTPBearer()


@router.get("/mobile/tree")
def get_tree_by_id(
    id: str = Query(..., alias="site", description="Site id"),
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return implantation_service.get_tree_by_id(id=id, token=token)


@router.get("/mobile/info")
def get_asset_info_by_id(
    id: str = Query(..., alias="site", description="Site id"),
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return implantation_service.get_asset_info_by_id(id=id, token=token)


@router.get("/mobile/static")
def get_static_asset(
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials

    return implantation_service.get_static_asset(token)


@router.get("/mobile/static/get_lubricants")
def get_lubricants(
    credentials: HTTPAuthorizationCredentials = Depends(implantation_scheme),
):
    token = credentials.credentials
    return implantation_service.get_lubricants(token)
