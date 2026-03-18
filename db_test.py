import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, Boolean, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
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
     staff_id = Column(Integer,ForeignKey("member.id"), nullable=True)
     ward_id = Column(Integer,ForeignKey("ward.id"), nullable=True)
     role = Column(Enum('Head_Nurse', 'Staff_Nurse', name='staff_role_enum'), nullable=False)
     level = Column(Enum('N0', 'N1', 'N2', 'N3', 'N4', name='staff_level_enum'), nullable=True)
     staff_info = relationship("member", back_populates="members")
     ward_info = relationship("ward", back_populates="wards")


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




staff_list = [
            ("謝0靜", "NUR0002", "NUR0002"),
            ("林0雯", "NUR0003", "NUR0003"),
            ("李0政", "NUR0004", "NUR0004"),
            ("李0庭", "NUR0005", "NUR0005"),
            ("朱0茜", "NUR0006", "NUR0006"),
            ("賴0珍", "NUR0007", "NUR0007"),
            ("林0均", "NUR0008", "NUR0008"),
            ("楊0閔", "NUR0009", "NUR0009"),
            ("譚0慈", "NUR0010", "NUR0010"),
            ("張0研", "NUR0011", "NUR0011"),
            ("吳0儀", "NUR0012", "NUR0012"),
            ("謝0?", "NUR0013", "NUR0013"),
            ("陳0宸", "NUR0014", "NUR0014"),
            ("江0芸", "NUR0015", "NUR0015"),
            ("張0文", "NUR0016", "NUR0016"),
            ("張0翔", "NUR0017", "NUR0017"),
            ("朱0碩", "NUR0018", "NUR0018"),
            ("王0金", "NUR0019", "NUR0019"),
            ("駱0君", "NUR0020", "NUR0020"),
            ("謝0欣", "NUR0021", "NUR0021"),
            ("廖0婷", "NUR0022", "NUR0022"),
            ("楊0萱", "NUR0023", "NUR0023"),
            ("謝0洵", "NUR0024", "NUR0024"),
        ]