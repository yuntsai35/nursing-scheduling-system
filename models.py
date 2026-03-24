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

     
class scheduled_member(Base):
     __tablename__ = "scheduled_member"

     id = Column(Integer, primary_key=True, autoincrement=True)
     schedule_id = Column(String(50))
     staff_id = Column(Integer, ForeignKey('member.id'))
     schedule_date = Column(Integer)
     leave_dates = Column(Text)
     ward_id = Column(Integer,ForeignKey("ward.id"))

     
class settingtime(Base):
     __tablename__ = "settingtime"

     id = Column(Integer, primary_key=True, autoincrement=True)
     ward_id = Column(Integer, ForeignKey("ward.id"), nullable=False)
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
     ward_id = Column(Integer,ForeignKey("ward.id"), nullable=False)

class finalscheduletable(Base):
    __tablename__ = "final_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("member.id"), nullable=False)   
    year_month = Column(String(20), nullable=False, index=True) 
    ward_id = Column(Integer, ForeignKey("ward.id"), nullable=False)     
    schedule_data = Column(JSONB, nullable=False) 
     
# if not exists,create
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




staff_list = [
            ("謝0靜", "nur0002", "nur0002"),
            ("林0雯", "nur0003", "nur0003"),
            ("李0政", "nur0004", "nur0004"),
            ("李0庭", "nur0005", "nur0005"),
            ("朱0茜", "nur0006", "nur0006"),
            ("賴0珍", "nur0007", "nur0007"),
            ("林0均", "nur0008", "nur0008"),
            ("楊0閔", "nur0009", "nur0009"),
            ("譚0慈", "nur0010", "nur0010"),
            ("張0研", "nur0011", "nur0011"),
            ("吳0儀", "nur0012", "nur0012"),
            ("謝0妤", "nur0013", "nur0013"),
            ("陳0宸", "nur0014", "nur0014"),
            ("江0芸", "nur0015", "nur0015"),
            ("張0文", "nur0016", "nur0016"),
            ("張0翔", "nur0017", "nur0017"),
            ("朱0碩", "nur0018", "nur0018"),
            ("王0金", "nur0019", "nur0019"),
            ("駱0君", "nur0020", "nur0020"),
            ("謝0欣", "nur0021", "nur0021"),
            ("廖0婷", "nur0022", "nur0022"),
            ("楊0萱", "nur0023", "nur0023"),
            ("謝0洵", "nur0024", "nur0024"),
        ]