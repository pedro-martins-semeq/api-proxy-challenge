from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api.auth.routes import router as auth_router
from app.api.usercorp.routes import router as usercorp_router
from app.api.implantation.routes import router as implantation_router


app = FastAPI(title="Proxy API")
bearer_scheme = HTTPBearer()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(usercorp_router, prefix="/usercorp", tags=["usercorp"])
app.include_router(implantation_router,
                   prefix="/implantation", tags=["implantation"])
