from sqlalchemy import Column, Integer, String, Boolean, Enum, DECIMAL, ForeignKey, LargeBinary, Date
from database import Base, Base2, Base3
import enum
import uuid

class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"

class Hostel(Base):
    __tablename__ = "hostels"
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostel_name = Column(String(225), nullable=False)
    area = Column(String(225), nullable=False)
    city = Column(String(225), nullable=False)
    state = Column(String(225), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone_number = Column(String(20), nullable=False)

    veg = Column(Boolean, default=False)
    non_veg = Column(Boolean, default=False)

    ac = Column(Boolean, default=False)
    non_ac = Column(Boolean, default=False)

    no_of_ac_beds = Column(Integer, default=0)
    no_of_non_ac_beds = Column(Integer, default=0)

    non_ac_sharing = Column(Boolean, default=False)
    non_ac_sharing_price = Column(DECIMAL(10,2), default=0.00)

    ac_sharing = Column(Boolean, default=False)
    ac_sharing_price = Column(DECIMAL(10,2), default=0.00)
    username = Column(String(100), unique=True)
    password = Column(String(500))

    terms_and_conditions = Column(String(500))
    rules_and_regulations = Column(String(500))

class Menu(Base):
    __tablename__ = 'menu'
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), ForeignKey('hostel_form.hostels.id'), primary_key=True)
    monday = Column(String(50))
    tuesday = Column(String(50))
    wednesday = Column(String(50))
    thursday = Column(String(50))
    friday = Column(String(50))
    saturday = Column(String(50))
    sunday = Column(String(50))


class WifiScreens(Base):
    __tablename__ = 'wifiscreens'
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), ForeignKey('hostel_form.hostels.id'), primary_key=True)

    screens = Column(String(50))
    password = Column(String(50))



###############################################################################################33333333333



class GovtIDEnum(str, enum.Enum):
    Aadhar = "Aadhar"
    PAN = "PAN"
    VoterID = "VoterID"

class NecessityEnum(str, enum.Enum):
    Student = "Student"
    Employee = "Employee"
    SelfEmployment = "Self Employee"
    Other = "Other"

class FoodEnum(str, enum.Enum):
    Veg = "Veg"
    NonVeg = "Non Veg"
    Both = "Both"
class RoomEnum(str, enum.Enum):
    AC = "AC"
    NONAC = "Non AC"

class TenantRegistration(Base2):
    __tablename__ = "tenant_registration_form"
    __table_args__ = {"schema": "tenant"}
    tenant_id = Column(String(225), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)
    father_name = Column(String(50))
    father_phone_number = Column(String(50))
    gender = Column(Enum(GenderEnum), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String(100))
    house_no = Column(String(50))
    street = Column(String(50))
    colony = Column(String(50))
    landmark = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    pincode = Column(String(20))
    country = Column(String(20), default="India")
    govt_id_type = Column(Enum(GovtIDEnum), nullable=False)
    govt_id_file = Column(LargeBinary, nullable=True)
    govt_id_number = Column(String(50), nullable=False)
    necessity = Column(Enum(NecessityEnum), nullable=False)
    emergency_contact = Column(String(15))
    food_preference = Column(Enum(FoodEnum), nullable=False)
    room_type = Column(Enum(RoomEnum), nullable=False)

class TenantStudent(Base2):
    __tablename__ = "tenant_studen"
    __table_args__ = {"schema": "tenant"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id"), primary_key=True)
    studying_at = Column(String(200), nullable=False)
    student_id_number = Column(String(50), nullable=False)
    id_card_photo = Column(LargeBinary)
    college_address = Column(String(50))
    city = Column(String(100))
    pincode = Column(String(10))
    phone_number = Column(String(15))
  
class TenantEmployee(Base2):
    __tablename__ = "tenant_employee"
    __table_args__ = {"schema": "tenant"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    company_name = Column(String(200), nullable=False)
    employee_id_number = Column(String(50), nullable=False)
    id_card_image = Column(LargeBinary)
    address = Column(String(50))
    city = Column(String(100))
    pincode = Column(String(10))
    phone_number = Column(String(15))

   

class TenantSelfEmployed(Base2):
    __tablename__ = "tenant_self_employed"
    __table_args__ = {"schema": "tenant"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    occupation = Column(String(200), nullable=False)
    alternate_number = Column(String(15))
    

class TenantOther(Base2):
    __tablename__ = "tenant_other"
    __table_args__ = {"schema": "tenant"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    description = Column(String(500))
    phone_number = Column(String(15))

##########################################################################################################

class Users(Base3):
    __tablename__ = 'authentication'
    id = Column(String(200), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(100))
    username = Column(String(100), nullable=False, unique=True)
    ph_no = Column(String(50))
    password = Column(String(300), nullable=False)
    token = Column(String(300))
    is_active = Column(Boolean, default=True)




