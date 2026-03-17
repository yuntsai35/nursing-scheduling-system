import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, Boolean, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True,pool_recycle=3600,pool_pre_ping=True)
Base = declarative_base()


class staff(Base):
     __tablename__ = "staff"

     id = Column(Integer, primary_key=True, autoincrement=True)
     full_name = Column(String(50), nullable=False)
     employee_num = Column(String(20), nullable=False, unique=True)
     password = Column(String(255), nullable=False)
         
        
     role = Column(Enum('IT_Admin', 'Head_Nurse', 'Staff_Nurse', name='staff_role_enum'), nullable=False)
     level = Column(Enum('N0', 'N1', 'N2', 'N3', 'N4', name='staff_level_enum'), nullable=True)
        
     ward = Column(String(20), nullable=True)
     join_date = Column(Date, nullable=True)
     is_temp_password = Column(Boolean, default=True)

     schedules = relationship("scheduled_member", backref="staff")

     
class scheduled_member(Base):
     __tablename__ = "scheduled_member"

     id = Column(Integer, primary_key=True, autoincrement=True)
     schedule_id = Column(String(50))
     staff_id = Column(Integer, ForeignKey('staff.id'))
     schedule_date = Column(Integer)
     leave_dates = Column(Text)
     ward = Column(String(50))

     
class settingtime(Base):
     __tablename__ = "settingtime"

     id = Column(Integer, primary_key=True, autoincrement=True)
     ward = Column(String(50), nullable=False)
     min_rest_2w = Column(DECIMAL(4, 1))
     min_rest_1m = Column(DECIMAL(5, 1))
     max_continuous_work = Column(DECIMAL(4, 1))
     max_shifts_1w = Column(DECIMAL(4, 1))


class staff_number_schedule(Base):
     __tablename__ = "staff_number_schedule"

     id = Column(Integer, primary_key=True, autoincrement=True)
     shift = Column(String(30), nullable=False)
     shift_staff_number = Column(Integer, nullable=False)
     staff_id = Column(Text)
     ward = Column(String(30), nullable=False)

class finalscheduletable(Base):
    __tablename__ = "final_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, nullable=False)   
    name = Column(String(50), nullable=False)    
    year_month = Column(String(20), nullable=False, index=True) 
    ward = Column(String(20), nullable=False)     
    schedule_data = Column(JSONB, nullable=False) 
     
# if not exists,create
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)