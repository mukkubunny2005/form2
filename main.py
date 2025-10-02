from fastapi import FastAPI
from routers import tenant_registration, login, hostel_registration
from database import  Base, engine2, engine3, engine, Base2, Base3


app = FastAPI()
Base.metadata.create_all(bind=engine)
Base2.metadata.create_all(bind=engine2)
Base3.metadata.create_all(bind=engine3)
app.include_router(hostel_registration.router)
app.include_router(tenant_registration.router)
app.include_router(login.router)