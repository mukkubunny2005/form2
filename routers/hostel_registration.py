from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from pydantic import BaseModel, Field
from models import Hostel, Menu, GenderEnum, WifiScreens
from passlib.context import CryptContext

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class HostelRequest(BaseModel):
    hostel_name: str = Field(...)
    area: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    gender: GenderEnum = Field(...)
    phone_number: str = Field(...)

    veg: bool = Field(default=False)
    non_veg: bool = Field(default=False)
    ac: bool = Field(default=False)
    non_ac: bool = Field(default=False)

    no_of_ac_beds: int = Field(default=0)
    no_of_non_ac_beds: int = Field(default=0)

    non_ac_sharing: bool = Field(default=False)
    non_ac_sharing_price: float = Field(default=8000.00)

    ac_sharing: bool = Field(default=False)
    ac_sharing_price: float = Field(default=5000.00)

    monday: str = Field(...)
    tuesday: str = Field(...)
    wednesday: str = Field(...)
    thursday: str = Field(...)
    friday: str = Field(...)
    saturday: str = Field(...)
    sunday: str = Field(...)

    username: str = Field(...)
    password: str = Field(...)

    wifi_screens: str = Field(...)
    wifi_password:str = Field(...)

    terms_and_conditions :str = Field(...)
    rules_and_regulations:str = Field(...)


db_dependency = Annotated[Session, Depends(get_db)]

ALGORITHM = 'HS256'
bcrypt_Context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/')
def hostel_registration_from(hostel_request: HostelRequest, db: db_dependency):
    hostel_form = Hostel(
        hostel_name=hostel_request.hostel_name,
        area=hostel_request.area,
        city=hostel_request.city,
        state=hostel_request.state,
        gender=hostel_request.gender,
        phone_number=hostel_request.phone_number,
        veg=hostel_request.veg,
        non_veg=hostel_request.non_veg,
        ac=hostel_request.ac,
        non_ac=hostel_request.non_ac,
        no_of_ac_beds=hostel_request.no_of_ac_beds,
        no_of_non_ac_beds=hostel_request.no_of_non_ac_beds,
        non_ac_sharing=hostel_request.non_ac_sharing,
        non_ac_sharing_price=hostel_request.non_ac_sharing_price,
        ac_sharing=hostel_request.ac_sharing,
        ac_sharing_price=hostel_request.ac_sharing_price,
        username=hostel_request.username,
        password=bcrypt_Context.hash(hostel_request.password),
        rules_and_regulations = hostel_request.rules_and_regulations,
        terms_and_conditions=hostel_request.terms_and_conditions
    )

    db.add(hostel_form)
    db.commit()
    db.refresh(hostel_form)

    menu = Menu(
        id=hostel_form.id,
        monday=hostel_request.monday,
        tuesday=hostel_request.tuesday,
        wednesday=hostel_request.wednesday,
        thursday=hostel_request.thursday,
        friday=hostel_request.friday,
        saturday=hostel_request.saturday,
        sunday=hostel_request.sunday
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)

    wifi = WifiScreens(
        id = hostel_form.id,
        screens = hostel_request.wifi_screens,
        password = hostel_request.wifi_password
    )
    db.add(wifi)
    db.commit()
    db.refresh(wifi)
    return hostel_form

##############################################  PERSON REGISTRATION ################################


