from fastapi import FastAPI
from routers import tenant_registration, login, hostel_registration
from database import  Base, engine2, engine3, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine2)
Base.metadata.create_all(bind=engine3)
app.include_router(hostel_registration.router)
app.include_router(tenant_registration.router)
app.include_router(login.router)