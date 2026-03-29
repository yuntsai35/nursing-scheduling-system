import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, Boolean, Text, DECIMAL, ForeignKey, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True,pool_recycle=3600,pool_pre_ping=True)
Base = declarative_base()

class member(Base):
     __tablename__ = "member"

     id = Column(Integer, primary_key=True, autoincrement=True)
     full_name = Column(String(50), nullable=False)
     employee_num = Column(String(20), nullable=False, unique=True)
     password = Column(String(255), nullable=False)
     members= relationship("member_ward", back_populates="staff_info")
 

class ward(Base):
     __tablename__ = "ward"

     id = Column(Integer, primary_key=True, autoincrement=True)
     ward_name = Column(String(50), nullable=False)
     wards= relationship("member_ward", back_populates="ward_info")



class member_ward(Base):
     __tablename__ = "member_ward"

     id = Column(Integer, primary_key=True, autoincrement=True)
     staff_id = Column(Integer,ForeignKey("member.id"), nullable=True, index=True)
     ward_id = Column(Integer,ForeignKey("ward.id"), nullable=True, index=True)
     role = Column(Enum('Head_Nurse', 'Staff_Nurse', name='staff_role_enum'), nullable=False)
     level = Column(Enum('N0', 'N1', 'N2', 'N3', 'N4', name='staff_level_enum'), nullable=True)
     staff_info = relationship("member", back_populates="members")
     ward_info = relationship("ward", back_populates="wards")

     
class scheduled_member(Base):
     __tablename__ = "scheduled_member"

     id = Column(Integer, primary_key=True, autoincrement=True)
     schedule_id = Column(String(50), index=True)
     staff_id = Column(Integer, ForeignKey('member.id'), index=True)
     schedule_date = Column(Integer)
     leave_dates = Column(Text)
     ward_id = Column(Integer,ForeignKey("ward.id"))

     __table_args__ = (
        Index('idx_ward_schedule', 'ward_id', 'schedule_id'),
    )

     
class settingtime(Base):
     __tablename__ = "settingtime"

     id = Column(Integer, primary_key=True, autoincrement=True)
     ward_id = Column(Integer, ForeignKey("ward.id"), nullable=False, index=True)
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
     ward_id = Column(Integer,ForeignKey("ward.id"), nullable=False, index=True)

    

class finalscheduletable(Base):
    __tablename__ = "final_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("member.id"), nullable=False)   
    year_month = Column(String(20), nullable=False) 
    ward_id = Column(Integer, ForeignKey("ward.id"), nullable=False)     
    schedule_data = Column(JSONB, nullable=False) 

    __table_args__ = (
        Index('idx_ward_year_month', 'ward_id', 'year_month'),
    )
     
# if not exists,create
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
