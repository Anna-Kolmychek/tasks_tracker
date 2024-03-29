from fastapi import FastAPI

from src.users.router import router as users_router
from src.positions.router import router as positions_router
from src.tasks.router import router as tasks_router
from src.services.router import router as services_router

app = FastAPI()


app.include_router(users_router)
app.include_router(positions_router)
app.include_router(tasks_router)
app.include_router(services_router)