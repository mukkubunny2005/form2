from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal2
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from models import GenderEnum, FoodEnum, RoomEnum, NecessityEnum, GovtIDEnum, TenantRegistration, TenantStudent, TenantEmployee, TenantSelfEmployed, TenantOther
import datetime
import io
router = APIRouter()

def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db2)]
from fastapi import Form

    

@router.post('/tenant_registration')
async def tenant_registration_form(
    db: db_dependency,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...),
    father_name: str = Form(...),
    father_phone_number: str = Form(...),
    gender: GenderEnum = Form(...),
    date_of_birth: datetime.date = Form(...),
    address: str = Form(...),
    house_no: str = Form(...),
    street: str = Form(...),
    colony: str = Form(...),
    landmark: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    country: str = Form("India"),
    govt_id_type: GovtIDEnum = Form(...),
    govt_id_number: str = Form(...),
    necessity: NecessityEnum = Form(...),
    emergency_contact: str = Form(...),
    food_preference: FoodEnum = Form(...),
    room_type: RoomEnum = Form(...),
    govt_id_file: UploadFile = File(...),
    
):
    # Create tenant object
    tenant = TenantRegistration(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        father_name=father_name,
        father_phone_number=father_phone_number,
        gender=gender,
        date_of_birth=date_of_birth,
        address=address,
        house_no=house_no,
        street=street,
        colony=colony,
        landmark=landmark,
        city=city,
        state=state,
        pincode=pincode,
        country=country,
        govt_id_type=govt_id_type,
        govt_id_number=govt_id_number,
        govt_id_file=await govt_id_file.read(),
        necessity=necessity,
        emergency_contact=emergency_contact,
        food_preference=food_preference,
        room_type=room_type,

    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)


    return {"message": "Tenant created", "tenant_id": tenant.tenant_id}
@router.post('/tenant_registration/student')
async def student_tenant(
    db:db_dependency,
    tenant_id :str ,
    studying_at : str ,
    student_id_number : str ,
    id_card_photo : UploadFile ,
    college_address : str ,
    city : str ,
    pincode: str ,
    phone_number: str 
    ):
    student = TenantStudent(
        tenant_id = tenant_id,
        studying_at = studying_at,
        student_id_number = student_id_number,
        id_card_photo = await id_card_photo.read(),
        college_address = college_address,
        city = city,
        pincode = pincode,
        phone_number = phone_number
    )
    db.add(student)
    db.commit()
    return "added successfully"

@router.post('/tenant_registration/employee')
async def tenant_employee(
    db:db_dependency,
    tenant_id : str ,
    company_name : str ,
    employee_id_number : str,
    id_card_image : UploadFile,
    address: str ,
    city : str ,
    pincode : str ,
    phone_number : str 

):
    employee = TenantEmployee(
        tenant_id = tenant_id,
        company_name = company_name,
        employee_id_number = employee_id_number,
        id_card_image =await id_card_image.read(),
        address = address,
        city = city,
        pincode = pincode,
        phone_number = phone_number
    )
    db.add(employee)
    db.commit()
    return 'added successfully'

@router.post('/tenant_registration/self-employee')
async def tenant_Self_employee(
    db:db_dependency,
    tenant_id : str,
    occupation : str,
    alternate_number : str
):
    self_employee = TenantSelfEmployed(
        tenant_id = tenant_id,
        occupation = occupation,
        alternate_number = alternate_number
    )
    db.add(self_employee)
    db.commit()
    return self_employee


@router.post('/tenant_registration/other')
async def tenant_other(
    db:db_dependency,
    tenant_id :str,
    description:str,
    phone_number:str
):
    other = TenantOther(
        tenant_id  = tenant_id,
        description = description,
        phone_number = phone_number
    )
    db.add(other)
    db.commit()
    return other

