from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI(title="Proxy API")
bearer_scheme = HTTPBearer()
