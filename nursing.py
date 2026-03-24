from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import datetime
from datetime import datetime, timezone, timedelta
import jwt
from cache import r
import json

import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from db_test import engine, Base, scheduled_member, settingtime, staff_number_schedule,finalscheduletable,member,ward,member_ward, SessionLocal
from sqlalchemy import desc,asc


from datetime import datetime
from decimal import Decimal

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/login.html", media_type="text/html")
@app.get("/index", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/main/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/main.html", media_type="text/html")
@app.get("/staff/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/staff.html", media_type="text/html")
@app.get("/setting/{ward_id}", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/setting.html", media_type="text/html")
@app.get("/setting1/{ward_id}", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/setting1.html", media_type="text/html")
@app.get("/settingmember/{ward_id}", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/settingmember.html", media_type="text/html")
@app.get("/settingfinal/{ward_id}", include_in_schema=False)
async def index(request: Request):    
	return FileResponse("./static/settingfinal.html", media_type="text/html")
@app.get("/mainreservebreak/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/mainreservebreak.html", media_type="text/html")
@app.get("/reservebreak/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/reservebreak.html", media_type="text/html")
@app.get("/mainfinalscheduling/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/mainfinalscheduling.html", media_type="text/html")
@app.get("/finalscheduling/{ward_id}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/finalscheduling.html", media_type="text/html")
@app.get("/membership", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/membership.html", media_type="text/html")




#會員
@app.post("/api/user/auth")
async def signup(request: Request, body: dict = Body(...)):
    db=SessionLocal()

    name=body["name"]
    employee_num=body["employee_num"].lower()
    password=body["password"]
 
    if not all([name,employee_num,password]):
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "建立失敗，欄位不可為空"}
            )
    
    result=db.query(member).filter(member.employee_num == employee_num).first()

    try:
        if result==None:
            stafflist = member(employee_num=employee_num, full_name=name, password=password)
            db.add(stafflist)
            db.commit()
            return{"ok":True}
        else:
            return JSONResponse(
				status_code=400,
				content={
					"error": True,
					"message": "註冊失敗，重複的員工編號"
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
                        "password": payload["password"]
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
    
    result=db.query(member).filter(member.employee_num == employee_num).filter(member.password==password).first()

    try:
        if result:
            payload={"id":result.id,"full_name":result.full_name,"employee_num":result.employee_num,"password":result.password, "exp": datetime.now(tz=timezone.utc) + timedelta(days=7)}
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
      
        import traceback
        traceback.print_exc() 
    
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": f"伺服器內部錯誤: {str(e)}"
            }
        )
    finally:
         db.close()

#新增病房群組
@app.post("/api/ward")
async def insertward(request: Request, body: dict = Body(...)):
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
    
    ward_name=body["ward_name"]

    try:
        new_ward = ward(ward_name=ward_name)
        db.add(new_ward)
        db.flush()
        combine=member_ward(staff_id=id,ward_id=new_ward.id,role='Head_Nurse')
        db.add(combine)
        db.commit()
        return{"ok":True}
    
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
    except Exception as e:
            print(f"CRITICAL DATABASE ERROR: {str(e)}")
            return JSONResponse(
				status_code=500,
				content={
					"error": True,
					"message": "伺服器內部錯誤"
				}
			)
    finally:
         db.close()

@app.get("/api/member_ward")
async def get_staff_list(request: Request):
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
        result=db.query(member_ward.role,member_ward.ward_id,ward.ward_name).join(ward, member_ward.ward_id == ward.id).filter(member_ward.staff_id == id).all()
        data_list = []
        for row in result:
            data_list.append({
                "role": row.role,
                "ward_id": row.ward_id,
                "ward_name":row.ward_name
            })

        return {"data":data_list}
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

@app.delete("/api/member_ward")
async def deletemember_ward(request:Request, body: dict = Body(...)):
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
    
    ward_id=body["ward_id"]
    results=db.query(member_ward.role).filter(member_ward.ward_id == ward_id,member_ward.staff_id==id, member_ward.role == 'Head_Nurse')
    if not results:
            return JSONResponse(status_code=403, content={"error": True, "message": "只有該病房的護理長可以刪除整個群組"})

    try:
        db.query(member_ward).filter(member_ward.ward_id == ward_id).delete()
        db.query(ward).filter(ward.id == ward_id).delete()
        db.commit()
        return {"ok":True}
        
    except jwt.PyJWTError: 
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    finally:
         db.close()
 

#要驗證是否登入及是否有在群組內
#員工管理
@app.get("/api/ward/{ward_id}/staff")
async def get_staff_list(request: Request, ward_id: int = None):
    cache_key = f"memeber_list:ward:{ward_id}"

    cached_data = r.get(cache_key)
    if cached_data:
        return {"data": json.loads(cached_data),"source": "redis"}
    
    
    
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
        results = db.query(member, member_ward.role, member_ward.level,ward.ward_name).join(member_ward, member.id == member_ward.staff_id).join(ward, member_ward.ward_id == ward.id).filter(member_ward.ward_id == ward_id, member_ward.role == 'Staff_Nurse').order_by(member.employee_num.asc()).all()

        data_list = []

        for user, role, level, ward_name in results:
            data_list.append({
                "id": user.id,
                "employee_num": user.employee_num,
                "full_name": user.full_name,
                "role": role, 
                "level": level,     
                "ward": ward_name
            })
         
        r.setex(cache_key, 3600, json.dumps(data_list))

        return {"data": data_list,"source": "sql"}
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
    
         
@app.post("/api/ward/{ward_id}/staff")
async def insertstaff(request: Request,ward_id: int, body: dict = Body(...)):
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
        stafflist = member(employee_num=staffid, full_name=name, password=staffid, role=role, level=level, ward=ward_id, join_date=joindate)
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
         

    
@app.delete("/api/ward/{ward_id}/staff")
async def deletestaff(request:Request,ward_id: int, body: dict = Body(...)):
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
        target = db.query(member).filter(member.id == staffid).first()
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
    

@app.patch("/api/ward/{ward_id}/staff")
async def editstaff(request:Request,ward_id: int, body: dict = Body(...)):
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
        
        target = db.query(member).filter(member.id == staffid).first()
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
    
#會員姓名及修改
@app.get("/api/memberinfo")
async def getmembership(request: Request):
    db = SessionLocal()  
    bearerToken = request.headers.get("Authorization")
    
    if not bearerToken:
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )

    try:
        token = bearerToken.split(" ")[1]
        payload = jwt.decode(token, os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        current_user_id = payload["id"]

        user_data = db.query(member).filter(member.id == current_user_id).first()

        if not user_data:
            return JSONResponse(
                status_code=404,
                content={"error": True, "message": "找不到該會員資料"}
            )


        return {"data": {
                "name": user_data.full_name,  
                "employee_num":user_data.employee_num,
                "staffid": user_data.id}}

    except jwt.PyJWTError: 
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "憑證無效或已過期"}
        )
    except Exception as e:
        print(f"抓取會員資料發生錯誤: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "伺服器內部錯誤"}
        )
    finally:
        db.close()  
     
#會員姓名及修改
@app.patch("/api/membership")
async def updatemembership(request: Request, body: dict = Body(...)):
    db = SessionLocal()
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

    try:
        current_user_id = payload["id"]
        data = db.query(member).filter(member.id == current_user_id).first()

        #改姓名
        if "name" in body and body["name"]:
            data.full_name = body["name"]
            db.commit()
            return {"ok": True, "message": "姓名修改成功"}

        #改密碼
        if "newpassword" in body:
            if data.password != body.get("oldpassword"):
                return JSONResponse(status_code=400, content={"error": True, "message": "舊密碼錯誤"})
            
            data.password = body["newpassword"]
            db.commit()
            return {"ok": True, "message": "密碼修改成功"}

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"error": True, "message": "儲存失敗"})
    finally:
        db.close()


#一次設定部分全部
@app.post("/api/ward/{ward_id}/setting")
async def updatesetting(request:Request, ward_id: int, body: dict = Body(...)):
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
    
    
    try:
        #settingtime
        min_rest_2w= float(body["min_rest_2w"])
        min_rest_1m= float(body["min_rest_1m"])
        max_continuous_work= float(body["max_continuous_work"])
        max_shifts_1w= float(body["max_shifts_1w"])

        #settingdate
        schedule_id= body["selectedDate"]
        staff_id= body["selectedStaff"]
        schedule_date= body["days"]
        
        #settingstaffnumber
        required_dayshift=int(body["required_dayshift"])
        required_nightshift=int(body["required_nightshift"])
        required_mignightshift=int(body["required_mignightshift"])

        selectedNightStaff=",".join(body["multi_selector"])
        selectedMidnightStaff=",".join(body["multi_selector_midnight"])
        
        #delete
        db.query(settingtime).filter(settingtime.ward_id == ward_id).delete()
        db.query(scheduled_member).filter(scheduled_member.schedule_id == schedule_id,scheduled_member.ward_id == ward_id).delete(synchronize_session=False)
        db.query(staff_number_schedule).filter(staff_number_schedule.ward_id == ward_id).delete(synchronize_session=False)
        
        #settingtimeadd
        new_settingtime = settingtime(ward_id=ward_id, min_rest_2w=min_rest_2w, min_rest_1m=min_rest_1m, max_continuous_work=max_continuous_work, max_shifts_1w=max_shifts_1w)
        db.add(new_settingtime)
       
        #settingdateadd
        db.query(scheduled_member).filter(scheduled_member.schedule_id == schedule_id,scheduled_member.ward_id == ward_id).delete(synchronize_session=False)
        
        for id in staff_id:
            new_record = scheduled_member(
                schedule_id=schedule_id,
                staff_id=id,
                schedule_date=schedule_date,
                ward_id=ward_id
            )
            db.add(new_record)
        
        #settingstaffnumber
        shifting_group=[("day",required_dayshift,"",ward_id),("night",required_nightshift,selectedNightStaff,ward_id),("midnight", required_mignightshift, selectedMidnightStaff,ward_id)]

        for data in shifting_group:     
             new_record = staff_number_schedule(shift=data[0],shift_staff_number=data[1],staff_id=data[2],ward_id=data[3])
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

#完成
@app.get("/api/ward/{ward_id}/date")
async def reservemonth(request: Request,ward_id: int):
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
      
    try:
        results = db.query(scheduled_member.schedule_id).filter(scheduled_member.ward_id==ward_id).distinct().order_by(scheduled_member.schedule_id.desc()).all()
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
    
#完成
@app.get("/api/ward/{ward_id}/reservestaff/{date}")
async def getreservestaff(request: Request,ward_id: int, date: str = None):
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

    try:
        results = db.query(
        scheduled_member.staff_id,
        scheduled_member.schedule_date,
        member.full_name,
        member_ward.level,
        scheduled_member.leave_dates).join(member, scheduled_member.staff_id == member.id).join(member_ward, (member.id == member_ward.staff_id) & (member_ward.ward_id == ward_id)).filter(scheduled_member.schedule_id == date,scheduled_member.ward_id == ward_id).all()
        formatted_data = []
        for row in results:
            formatted_data.append({
                "staff_id": row.staff_id,
                "schedule_date": row.schedule_date,
                "full_name": row.full_name,
                "level": row.level,
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


#完成
from ortools.sat.python import cp_model
@app.post("/api/ward/{ward_id}/finalscheduling/{date}")
async def final_scheduling(request: Request,ward_id: int, date: str = None):
    db = SessionLocal()
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
    
    try:
        # 人員資料,職級與請假日期
        members = db.query(scheduled_member, member.full_name, scheduled_member.staff_id, scheduled_member.leave_dates).join(member, scheduled_member.staff_id == member.id).filter(scheduled_member.ward_id == ward_id, scheduled_member.schedule_id == date).all()
        
        # 時間需求
        time_setting = db.query(settingtime).filter(settingtime.ward_id == ward_id).first()
        #每班人數限制
        staff_number_day=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="day", staff_number_schedule.ward_id == ward_id)
        staff_number_night=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="night",staff_number_schedule.ward_id == ward_id)
        staff_number_midnight=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="midnight",staff_number_schedule.ward_id == ward_id)
        #包班限制
        staff_list_day=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="day", staff_number_schedule.ward_id == ward_id).first()
        staff_list_night=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="night",staff_number_schedule.ward_id == ward_id).first()
        staff_list_midnight=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="midnight",staff_number_schedule.ward_id == ward_id).first()


        # 人數
        num_nurses = len(members)
        # 該月總天數
        num_days = int(members[0][0].schedule_date) 
        num_shifts=4
        
        all_nurses = range(num_nurses)
        all_shifts = range(num_shifts) # 0:休, 1:D, 2:E, 3:N
        all_days = range(num_days)

        #n=每個護理師 d=天數 s=班別
        model = cp_model.CpModel()
        shifts = {}
        for n in all_nurses:
            for d in all_days:
                for s in all_shifts:
                    shifts[(n, d, s)] = model.NewBoolVar(f'n{n}_d{d}_s{s}')

        # 每人每天只能有一個班次
        for n in all_nurses:
            for d in all_days:
                model.AddExactlyOne(shifts[(n, d, s)] for s in all_shifts)

        staff_number_day= staff_number_day.scalar() # 白班
        staff_number_night= staff_number_night.scalar() # 小夜
        staff_number_midnight= staff_number_midnight.scalar() # 大夜

        
        #每班人數限制
        for d in all_days:
            model.Add(sum(shifts[(n, d, 1)] for n in all_nurses) == staff_number_day) # 白班
            model.Add(sum(shifts[(n, d, 2)] for n in all_nurses) == staff_number_night) # 小夜
            model.Add(sum(shifts[(n, d, 3)] for n in all_nurses) == staff_number_midnight) # 大夜
        
        #請假及包班規畫 人數、班數、天數
        #空的格子
        shift_requests = [] 
        for n in all_nurses:
            days = [] # 每個人幾天有幾個
            for d in all_days:
                day_shifts = [0, 0, 0, 0] # 班數
                days.append(day_shifts)
            shift_requests.append(days)
        
        #建立名字數字對照表
        name_to_index = {}
        for n in all_nurses:
            nurse_name = members[n][1] 
            name_to_index[nurse_name] = n

        #包小夜
        if staff_list_night and staff_list_night[0]:
            staff_list_night=staff_list_night[0].split(',')
            for name_night in staff_list_night:
                ind_night=name_to_index.get(name_night)
                if ind_night is not None:
                    for d in all_days:
                        shift_requests[ind_night][d][2] = 1

        #包大夜
        if staff_list_midnight and staff_list_midnight[0]:
            staff_list_midnight=staff_list_midnight[0].split(',')
            for name_midnight in staff_list_midnight:
                ind_midnight=name_to_index.get(name_midnight)
                if ind_midnight is not None:
                    for d in all_days:
                        shift_requests[ind_midnight][d][3] = 1
             
             
        #抓請假
        for n in all_nurses:
            day=members[n][3]
            days_off=[]
            if day:
                leave_day_list=day.split(',')
                for item in leave_day_list:
                    day_number = int(item)
                    index = day_number - 1
                    days_off.append(index)
            for item in days_off:
                 shift_requests[n][item][0]=1
                    

        #勞務平衡
        num_shifts= staff_number_day+staff_number_night+staff_number_midnight
        min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
        if num_shifts * num_days % num_nurses == 0:
            max_shifts_per_nurse = min_shifts_per_nurse
        else:
            max_shifts_per_nurse = min_shifts_per_nurse + 1
        for n in all_nurses:
            shifts_worked = []
            for d in all_days:
                for s in [1,2,3]:
                    shifts_worked.append(shifts[(n, d, s)])
            model.Add(min_shifts_per_nurse <= sum(shifts_worked))
            model.Add(sum(shifts_worked) <= max_shifts_per_nurse)

        #settingtime限制
        for n in all_nurses:
            # 月休天數限制
            model.Add(sum(shifts[(n, d, 0)] for d in all_days) >= int(time_setting.min_rest_1m))
            
            # 連續工作天數限制
            for d in range(num_days - int(time_setting.max_continuous_work)):
                model.Add(sum(shifts[(n, d + i, 0)] for i in range(int(time_setting.max_continuous_work) + 1)) >= 1)

            # 班次間隔限制 (禁止 E/N 接 D)
            for d in range(num_days - 1):
                model.Add(shifts[(n, d, 2)] + shifts[(n, d + 1, 1)] <= 1)
                model.Add(shifts[(n, d, 3)] + shifts[(n, d + 1, 1)] <= 1)

            #兩周內最少休息天數
            for d in range(num_days - 13):
                model.Add(sum(shifts[(n, d + i, 0)] for i in range(14)) >= time_setting.min_rest_2w)
            
            #先不處理一周內班別限制 處理包班就好

        model.Maximize(
        sum(
            shift_requests[n][d][s] * shifts[(n, d, s)]
            for n in all_nurses
            for d in all_days
            for s in all_shifts))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 20.0 # 給予更多運算時間
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL:
            # 整理與儲存資料
            organized_storage = {}
            for n in all_nurses:
                staff_id = members[n][2]

                personal_schedule={}
                for d in all_days:
                    for s in all_shifts:
                        if solver.Value(shifts[(n, d, s)]) == 1:
                            personal_schedule[str(d + 1)] = s
                
                organized_storage[staff_id] = personal_schedule

        

            # 寫入資料庫
            db.query(finalscheduletable).filter(finalscheduletable.ward_id == ward_id, finalscheduletable.year_month == date).delete()

            for staff_id, schedule_json in organized_storage.items():
                new_record = finalscheduletable(staff_id=staff_id,year_month=date, ward_id=ward_id, schedule_data=schedule_json)
                db.add(new_record)
            
            db.commit()
            return {"ok": True}
        else:
            return {"status": "error", "message": "在放寬限制後仍找不到可行解，請檢查總人力是否充足"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"系統錯誤: {str(e)}"}
    finally:
        db.close()
    
#完成
@app.get("/api/ward/{ward_id}/finalmonth")
async def finalmonth(request: Request,ward_id: int):
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
    
    try:
        results = db.query(finalscheduletable.year_month).filter(finalscheduletable.ward_id==ward_id).distinct().order_by(finalscheduletable.year_month.desc()).all()
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


#完成
#抓date資料
@app.get("/api/ward/{ward_id}/finalstaff/{date}")
async def getreservestaff(request: Request, ward_id: int, date: str = None):
    db=SessionLocal()
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統"})

    try:
        token = bearerToken.split(" ")[1]
        payload = jwt.decode(token, os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])



        results = db.query(finalscheduletable.staff_id, member.full_name, member_ward.level, finalscheduletable.schedule_data).join(member,finalscheduletable.staff_id == member.id).join(member_ward,(member.id==member_ward.staff_id)&(member_ward.ward_id==ward_id)).filter(finalscheduletable.year_month == date,finalscheduletable.ward_id == ward_id).all()
        formatted_data = []
        for row in results:
            formatted_data.append({
                "id":row.staff_id,
                "full_name": row.full_name,
                "level": row.level,
                "schedule_date": row.schedule_data
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

