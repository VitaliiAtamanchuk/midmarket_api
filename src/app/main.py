from fastapi import Depends
from fastapi import FastAPI

from app.core.deps import get_api_key
from app.currency.endpoints import router as currency_router


app = FastAPI(dependencies=[Depends(get_api_key)])
app.include_router(currency_router)
