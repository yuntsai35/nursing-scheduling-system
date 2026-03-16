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
from db_test import engine, Base, staff, scheduled_member, settingtime, staff_number_schedule,finalscheduletable, SessionLocal
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
@app.get("/mainreservebreak", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/mainreservebreak.html", media_type="text/html")
@app.get("/reservebreak", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/reservebreak.html", media_type="text/html")
@app.get("/mainfinalscheduling", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/mainfinalscheduling.html", media_type="text/html")
@app.get("/finalscheduling", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/finalscheduling.html", media_type="text/html")



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
        if role == 'generalstaff':
             results=db.query(staff).filter(staff.role =='Staff_Nurse').order_by(asc(staff.employee_num)).all()
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
        
        min_rest_2w= float(body["min_rest_2w"])
        min_rest_1m= float(body["min_rest_1m"])
        max_continuous_work= float(body["max_continuous_work"])
        max_shifts_1w= float(body["max_shifts_1w"])

        db.query(settingtime).filter(settingtime.ward == ward).delete()
        
        new_settingtime = settingtime(ward=ward,min_rest_2w=min_rest_2w,min_rest_1m=min_rest_1m,max_continuous_work=max_continuous_work,max_shifts_1w=max_shifts_1w)
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

#看要不要刪除
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
        staff.level,
        scheduled_member.leave_dates).join(staff, scheduled_member.staff_id == staff.id).filter(scheduled_member.schedule_id == date,scheduled_member.ward == ward).all()
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

#自動排班功能之後要將get改成post
from ortools.sat.python import cp_model

@app.post("/api/finalscheduling/{date}")
async def final_scheduling(request: Request, date: str = None):
    db = SessionLocal()
    ward = "N17"
    
    try:
        # 人員資料,職級與請假日期
        members = db.query(scheduled_member, staff.full_name, staff.level, scheduled_member.staff_id, scheduled_member.leave_dates).join(staff, scheduled_member.staff_id == staff.id).filter(scheduled_member.ward == ward, scheduled_member.schedule_id == date).all()
        
        # 時間需求
        time_setting = db.query(settingtime).filter(settingtime.ward == ward).first()
        #每班人數限制
        staff_number_day=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="day", staff_number_schedule.ward == ward)
        staff_number_night=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="night",staff_number_schedule.ward == ward)
        staff_number_midnight=db.query(staff_number_schedule.shift_staff_number).filter(staff_number_schedule.shift=="midnight",staff_number_schedule.ward == ward)
        #包班限制
        staff_list_day=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="day", staff_number_schedule.ward == ward).one()
        staff_list_night=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="night",staff_number_schedule.ward == ward).one()
        staff_list_midnight=db.query(staff_number_schedule.staff_id).filter(staff_number_schedule.shift=="midnight",staff_number_schedule.ward == ward).one()


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
        if staff_list_night[0]:
            staff_list_night=staff_list_night[0].split(',')
            for name_night in staff_list_night:
                ind_night=name_to_index.get(name_night)
                if ind_night is not None:
                    for d in all_days:
                        shift_requests[ind_night][d][2] = 1

        #包大夜
        if staff_list_midnight[0]:
            staff_list_midnight=staff_list_midnight[0].split(',')
            for name_midnight in staff_list_midnight:
                ind_midnight=name_to_index.get(name_midnight)
                if ind_midnight is not None:
                    for d in all_days:
                        shift_requests[ind_midnight][d][3] = 1
             
             
        #抓請假
        for n in all_nurses:
            day=members[n].leave_dates
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
                nurse_name = members[n][1]
                staff_id = members[n][3]
                organized_storage[nurse_name] = {"id": staff_id, "data": {}}
                for d in all_days:
                    for s in all_shifts:
                        if solver.Value(shifts[(n, d, s)]) == 1:
                            organized_storage[nurse_name]["data"][str(d + 1)] = s

        

            # 寫入資料庫
            db.query(finalscheduletable).filter(finalscheduletable.ward == ward, finalscheduletable.year_month == date).delete()

            for name, info in organized_storage.items():
                new_record = finalscheduletable(staff_id=info["id"],name=name,year_month=date, ward=ward, schedule_data=info["data"])
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
    
@app.get("/api/finalmonth")
async def finalmonth(request: Request):
    db=SessionLocal()
    try:
        results = db.query(finalscheduletable.year_month).distinct().order_by(finalscheduletable.year_month.desc()).all()
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


#抓date資料
@app.get("/api/finalstaff/{date}")
async def getreservestaff(request: Request,date: str = None):
    db=SessionLocal()
    ward = "N17"

    try:
        results = db.query(finalscheduletable.staff_id, staff.full_name,staff.level, finalscheduletable.schedule_data).join(staff, finalscheduletable.staff_id == staff.id).filter(finalscheduletable.year_month == date,finalscheduletable.ward == ward).all()
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

