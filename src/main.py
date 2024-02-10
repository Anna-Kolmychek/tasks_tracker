from fastapi import FastAPI

from src.users.router_users import router as users_router
from src.users.router_positions import router as positions_router

app = FastAPI()


app.include_router(users_router)
app.include_router(positions_router)
