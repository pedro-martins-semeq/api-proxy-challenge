from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api.auth.routes import router as auth_router


app = FastAPI(title="Proxy API")
bearer_scheme = HTTPBearer()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
