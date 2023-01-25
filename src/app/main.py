from fastapi import FastAPI, Depends

from app.currency.endpoints import router as currency_router
from app.core.deps import get_api_key


app = FastAPI(dependencies=[Depends(get_api_key)])
app.include_router(currency_router)
