from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import datetime
from datetime import timezone
import jwt

import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from db_test import engine, Base, staff, scheduled_member, settingtime, staff_number_schedule, SessionLocal
from sqlalchemy import desc,asc

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/login.html", media_type="text/html")
@app.get("/main", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/main.html", media_type="text/html")
@app.get("/staff", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/staff.html", media_type="text/html")
@app.get("/setting", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/setting.html", media_type="text/html")
@app.get("/setting1", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/setting1.html", media_type="text/html")
@app.get("/settingmember", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/settingmember.html", media_type="text/html")
@app.get("/membership", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/membership.html", media_type="text/html")
@app.get("/mainreservebreak", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/mainreservebreak.html", media_type="text/html")
@app.get("/reservebreak", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/reservebreak.html", media_type="text/html")



#會員
@app.get("/api/user/auth")
async def checkLoginStatus(request:Request):
    bearerToken = request.headers.get("Authorization")
    if bearerToken:
        try:
            token = bearerToken.split(" ")

            payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
            return {
                    "data": {
                        "id": payload["id"],
                        "full_name": payload["full_name"],
                        "employee_num": payload["employee_num"],
                        "password": payload["password"],
                        "role":payload["role"],
                        "ward":payload["ward"]
                    }
                }
        except(jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return {"data": None}

    else:
        return {"data": None}

@app.put("/api/user/auth")
async def login(request:Request,body: dict = Body(...)):
    db = SessionLocal()
    
    employee_num=body["employee_num"]
    password=body["password"]
    
    result=db.query(staff).filter(staff.employee_num == employee_num).filter(staff.password==password).first()

    try:
        if result:
            payload={"id":result.id,"full_name":result.full_name,"employee_num":result.employee_num,"password":result.password,"role":result.role,"ward":result.ward, "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=7)}
            token = jwt.encode(payload, os.getenv("SECRET_PASSWORD"), algorithm='HS256')
            return {"token": token}
        
        else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": True,
                        "message": "登入失敗，帳號或密碼錯誤或其他原因"
                    }
                )

    except Exception as e:
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()
 


#員工管理
@app.get("/api/staff/{role}")
async def get_staff_list(request: Request, role: str = None):
    db=SessionLocal()
    try:
        if role == 'adminstaff':
             results=db.query(staff).filter(staff.role =='Head_Nurse').order_by(asc(staff.employee_num)).all()
        else:
             results=db.query(staff).filter(staff.role =='Staff_Nurse').order_by(asc(staff.employee_num)).all()
        
        return {"data": results}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()
    
         
@app.post("/api/staff")
async def insertstaff(request: Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")

        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        id = payload["id"]
    
    staffid=body["staffid"]
    name=body["name"]
    role=body["role"]
    level=body["level"]
    ward=body["ward"]
    joindate=body["joindate"]
    password=body["staffid"]

    joindate=joindate.split('T')[0]

    if level == "無職級":
         level= None

    if not all([staffid,name,role,ward,joindate]):
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "建立失敗，輸入不正確或其他原因"}
            )

    try:
        stafflist = staff(employee_num=staffid, full_name=name, password=staffid, role=role, level=level, ward=ward, join_date=joindate)
        db.add(stafflist)
        db.commit()
        return{"ok":True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()
         

    
@app.delete("/api/staff")
async def deletestaff(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        id = payload["id"]
    
    staffid=body["staffid"]

    try:
        target = db.query(staff).filter(staff.id == staffid).first()
        db.delete(target)
        db.commit()
        return {"ok":True}
        
    except jwt.PyJWTError: 
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    finally:
         db.close()
    

@app.patch("/api/staff")
async def editstaff(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        id = payload["id"]

    try:
        staffid=body["staffid"]
        name=body["name"]
        role=body["role"]
        level=body["level"]
        ward=body["ward"]
        joindate=body["joindate"]
        if level == "無職級":
             level = None
        
        target = db.query(staff).filter(staff.id == staffid).first()
        target.full_name = name
        target.role = role
        target.level = level
        target.ward = ward
        target.join_date = joindate
        db.commit()
        return {"ok": True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"後端發生錯誤：{e}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()
    

@app.post("/api/settingtime")
async def updatesettingtime(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward=payload["ward"]

    try:
        min_shift_interval= float(body["min_shift_interval"])
        min_rest_2w= float(body["min_rest_2w"])
        min_rest_1m= float(body["min_rest_1m"])
        max_hours_1w= float(body["max_hours_1w"])
        max_hours_1d= float(body["max_hours_1d"])
        max_continuous_work= float(body["max_continuous_work"])
        max_shifts_1w= float(body["max_shifts_1w"])

        db.query(settingtime).filter(settingtime.ward == ward).delete()
        
        new_settingtime = settingtime(ward=ward,min_shift_interval=min_shift_interval,min_rest_2w=min_rest_2w,min_rest_1m=min_rest_1m,max_hours_1w=max_hours_1w,max_hours_1d=max_hours_1d,max_continuous_work=max_continuous_work,max_shifts_1w=max_shifts_1w)
        db.add(new_settingtime)
        db.commit()
        return {"ok": True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"後端發生錯誤：{e}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()


@app.get("/api/settingtime")
async def savesettingtime(request: Request):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward = payload["ward"]

    try:
        result=db.query(settingtime).filter(settingtime.ward==ward).first()
        return {"data":result}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()
    
@app.get("/api/settingmember")
async def savesettingtime(request: Request):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward = payload["ward"]

    try:
        result=db.query(settingtime).filter(settingtime.ward==ward).first()
        
        return {"data":result}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()
    
@app.get("/api/staff")
async def showstaff(request: Request):
    db=SessionLocal()
    try:
        results = db.query(staff).filter(staff.role == 'Staff_Nurse').all()
       
        data_list = []
        for user in results:
            data_list.append({
                "id": user.id,
                "full_name": user.full_name
            })
        
        return {"data": data_list}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()

@app.post("/api/settingmember")
async def updatesettingmember(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward=payload["ward"]

    try:
        schedule_id= body["selectedDate"]
        staff_id= body["selectedStaff"]
        schedule_date= body["days"]

        db.query(scheduled_member).filter(scheduled_member.schedule_id == schedule_id,scheduled_member.ward == ward).delete(synchronize_session=False)
        
        for id in staff_id:
            new_record = scheduled_member(
                schedule_id=schedule_id,
                staff_id=id,
                schedule_date=schedule_date,
                ward=ward
            )
            db.add(new_record)
        
        db.commit()
        
        return {"ok": True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"後端發生錯誤：{e}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()
    
#目前為固定的版本，請修改成彈性可增加項目的樣子
@app.post("/api/settingstaffnumber")
async def insertsettingstaffnumber(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward=payload["ward"]

    try:
        required_dayshift=int(body["required_dayshift"])
        required_nightshift=int(body["required_nightshift"])
        required_mignightshift=int(body["required_mignightshift"])

        selectedNightStaff=",".join(body["multi_selector"])
        selectedMidnightStaff=",".join(body["multi_selector_midnight"])

        db.query(staff_number_schedule).filter(staff_number_schedule.ward == ward).delete(synchronize_session=False)


        shifting_group=[("day",required_dayshift,"",ward),("night",required_nightshift,selectedNightStaff,ward),("midnight", required_mignightshift, selectedMidnightStaff,ward)]

        for data in shifting_group:     
             new_record = staff_number_schedule(shift=data[0],shift_staff_number=data[1],staff_id=data[2],ward=data[3])
             db.add(new_record)
        
        db.commit()
        return {"ok": True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"後端發生錯誤：{e}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()

@app.get("/api/date")
async def reservemonth(request: Request):
    db=SessionLocal()
    try:
        results = db.query(scheduled_member.schedule_id).distinct().order_by(scheduled_member.schedule_id.desc()).all()
        date_list = []
        for result in results:
            date_list.append(result[0])
        
        return {
            "data": {
                "date": date_list
            }
        }
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()
    

@app.get("/api/reservestaff/{date}")
async def getreservestaff(request: Request,date: str = None):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        ward = payload["ward"]

    try:
        results = db.query(
        scheduled_member.staff_id,
        scheduled_member.schedule_date,
        staff.full_name,
        scheduled_member.leave_dates).join(staff, scheduled_member.staff_id == staff.id).filter(scheduled_member.schedule_id == date,scheduled_member.ward == ward).all()
        formatted_data = []
        for row in results:
            formatted_data.append({
                "staff_id": row.staff_id,
                "schedule_date": row.schedule_date,
                "full_name": row.full_name,
                "leave_dates": row.leave_dates
            })
            
        return {"data": formatted_data}
    except HTTPException:
            raise HTTPException( 
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    finally:
         db.close()

@app.patch("/api/settingReserveBreak")
async def updateReserveBreak(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(
				status_code=403,
				content={
					"error": True,
					"message": "未登入系統，拒絕存取"})

    if bearerToken:
        token = bearerToken.split(" ")
        payload = jwt.decode(token[1], os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        id=payload["id"]
        ward=payload["ward"]

    try:
        leave_dates = body["reserve_dates"]
        schedule_id = body["schedule_id"]

        
        target = db.query(scheduled_member).filter(scheduled_member.staff_id == id,scheduled_member.ward == ward,scheduled_member.schedule_id == schedule_id).first()
        target.leave_dates = leave_dates
        db.commit()
        return {"ok": True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"後端發生錯誤：{e}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()
     