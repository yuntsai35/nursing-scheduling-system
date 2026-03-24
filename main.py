from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from controllers import auth, ward_controller, schedule
import datetime
from datetime import datetime, timezone, timedelta
import jwt
from cache import r
import json

import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from models import engine, Base, scheduled_member, settingtime, staff_number_schedule,finalscheduletable,member,ward,member_ward, SessionLocal
from sqlalchemy import desc,asc
import models 
models.Base.metadata.create_all(bind=engine)


from datetime import datetime
from decimal import Decimal


app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)    
app.include_router(ward_controller.router)
app.include_router(schedule.router)



@app.get("/", include_in_schema=False)
async def login(request: Request):
	return FileResponse("./static/login.html", media_type="text/html")
@app.get("/index", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/main/{ward_id}", include_in_schema=False)
async def main(request: Request):
	return FileResponse("./static/main.html", media_type="text/html")
@app.get("/staff/{ward_id}", include_in_schema=False)
async def staff(request: Request):
	return FileResponse("./static/staff.html", media_type="text/html")
@app.get("/setting/{ward_id}", include_in_schema=False)
async def setting(request: Request):    
	return FileResponse("./static/setting.html", media_type="text/html")
@app.get("/setting1/{ward_id}", include_in_schema=False)
async def setting1(request: Request):    
	return FileResponse("./static/setting1.html", media_type="text/html")
@app.get("/settingmember/{ward_id}", include_in_schema=False)
async def settingmemberx(request: Request):    
	return FileResponse("./static/settingmember.html", media_type="text/html")
@app.get("/settingfinal/{ward_id}", include_in_schema=False)
async def settingfinal(request: Request):    
	return FileResponse("./static/settingfinal.html", media_type="text/html")
@app.get("/mainreservebreak/{ward_id}", include_in_schema=False)
async def mainreservebreak(request: Request):
	return FileResponse("./static/mainreservebreak.html", media_type="text/html")
@app.get("/reservebreak/{ward_id}", include_in_schema=False)
async def reservebreak(request: Request):
	return FileResponse("./static/reservebreak.html", media_type="text/html")
@app.get("/mainfinalscheduling/{ward_id}", include_in_schema=False)
async def mainfinalscheduling(request: Request):
	return FileResponse("./static/mainfinalscheduling.html", media_type="text/html")
@app.get("/finalscheduling/{ward_id}", include_in_schema=False)
async def finalscheduling(request: Request):
	return FileResponse("./static/finalscheduling.html", media_type="text/html")
@app.get("/membership", include_in_schema=False)
async def membership(request: Request):
	return FileResponse("./static/membership.html", media_type="text/html")
