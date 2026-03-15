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

#自動排班功能之後要將get改成post喔
from ortools.sat.python import cp_model

@app.post("/api/finalscheduling/{date}")
async def final_scheduling(request: Request, date: str = None):
    db = SessionLocal()

    ward="N17"
    
    #主要排班的成員需求
    members = db.query(scheduled_member, staff.full_name).\
        join(staff, scheduled_member.staff_id == staff.id).\
        filter(scheduled_member.ward == ward, 
               scheduled_member.schedule_id == date).all()

    #時間需求
    time = db.query(settingtime).filter(settingtime.ward == ward).first()
    
    #三班需求
    requirements = db.query(staff_number_schedule).filter(
        staff_number_schedule.ward == ward
    ).all()

    num_nurses = len(members)
    num_shifts = len(requirements)+1
    num_days = int(members[0][0].schedule_date)
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    model = cp_model.CpModel()

    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar(f'n{n}_d{d}_s{s}')

    
    # (休 + 早 + 中 + 晚) 只能有一個是 1
    for n in all_nurses:
        for d in all_days:
            # 更加語意化，且執行效能通常較優
            model.add_exactly_one(shifts[(n, d, s)] for s in all_shifts)
        
    #每天白班要有6個人
    for d in all_days:
        # 白班 (s=1) 要 6 人
        model.Add(sum(shifts[(n, d, 1)] for n in all_nurses) == 6)
        
        # 小夜 (s=2) 要 4 人
        model.Add(sum(shifts[(n, d, 2)] for n in all_nurses) == 4)
        
        # 大夜 (s=3) 要 3 人
        model.Add(sum(shifts[(n, d, 3)] for n in all_nurses) == 3)
    
    # 一個月內必須有的最少休息天數
    min_off_1m = int(time.min_rest_1m) # 9
    for n in all_nurses:
        # 加總所有休假天數 (s=0) 必須 >= 9
        model.Add(sum(shifts[(n, d, 0)] for d in all_days) >= min_off_1m)

    # 連續工作上限，第 7 天強制休息
    max_consecutive = int(time.max_continuous_work) # 6
    for n in all_nurses:
        for d in range(num_days - max_consecutive):
            # 在任意連續的 7 天內，至少要有一天是休假 (s=0)
            model.Add(sum(shifts[(n, d + i, 0)] for i in range(max_consecutive + 1)) >= 1)
        
    # 勞基法 14 天內應有 4 天休息 (例假+休息日)
    min_off_2w = int(time.min_rest_2w) # 4
    for n in all_nurses:
        for d in range(num_days - 13):
            # 任意連續 14 天內，休假天數 (s=0) 必須 >= 4
            model.Add(sum(shifts[(n, d + i, 0)] for i in range(14)) >= min_off_2w)
    
    #班次最短間隔時數
    for n in all_nurses:
        for d in range(num_days - 1):
            # 如果第 d 天上小夜 (s=2)，第 d+1 天不能上白班 (s=1)
            model.Add(shifts[(n, d, 2)] + shifts[(n, d + 1, 1)] <= 1)
            # 如果第 d 天上大夜 (s=3)，第 d+1 天不能上白班 (s=1)
            model.Add(shifts[(n, d, 3)] + shifts[(n, d + 1, 1)] <= 1)
        
    for n in all_nurses:
        for d in range(num_days - 6):
            # 任意 7 天內，上班總數 (s != 0) 不得超過 5 班
            # 換句話說，休假 (s=0) 必須 >= 2 天
            model.Add(sum(shifts[(n, d + i, 0)] for i in range(7)) >= 2)
    
    for n in all_nurses:
        for d in range(num_days - 6): # 以每一週為滑動視窗
            # 建立三個輔助變數，代表這 7 天內有沒有上過 s=1, 2, 3 班
            used_s1 = model.NewBoolVar(f'used_s1_n{n}_d{d}')
            used_s2 = model.NewBoolVar(f'used_s2_n{n}_d{d}')
            used_s3 = model.NewBoolVar(f'used_s3_n{n}_d{d}')

            for i in range(7):
                # 邏輯連結：如果第 d+i 天上了 s=1，則 used_s1 必須為 1
                model.Add(used_s1 >= shifts[(n, d + i, 1)])
                model.Add(used_s2 >= shifts[(n, d + i, 2)])
                model.Add(used_s3 >= shifts[(n, d + i, 3)])

            # 核心限制：這三種班別的開關加起來，不能超過你設定的「2」
            model.Add(used_s1 + used_s2 + used_s3 <= 2)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        final_schedule = []
        for d in all_days:
            day_data = {"day": d + 1, "staff": []}
            for n in all_nurses:
                nurse_name = members[n][1] # 從你之前的 query 拿名字
                for s in all_shifts:
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        # 0:休, 1:早, 2:中, 3:晚 (根據你的 requirements 排序)
                        day_data["staff"].append({
                            "name": nurse_name,
                            "shift_type": s
                        })
            final_schedule.append(day_data)
    
        try:
            # A. 執行資料轉換：從「天」結構轉成「人」結構
            organized_storage = {}
            for day_entry in final_schedule:
                d_str = str(day_entry["day"])
                for s_info in day_entry["staff"]:
                    name = s_info["name"]
                    if name not in organized_storage:
                        # 從 members 中找到對應的 staff_id
                        sid = next(m[0].staff_id for m in members if m[1] == name)
                        organized_storage[name] = {"id": sid, "data": {}}
                    organized_storage[name]["data"][d_str] = s_info["shift_type"]

            # B. 寫入資料庫 (一人一列)
            # 建議先刪除該月份舊班表，避免重複存檔
            db.query(finalscheduletable).filter(
                finalscheduletable.ward == ward, 
                finalscheduletable.year_month == date
            ).delete()

            for name, info in organized_storage.items():
                new_record = finalscheduletable(
                    staff_id=info["id"],
                    name=name,
                    year_month=date,
                    ward=ward,
                    schedule_data=info["data"] # PostgreSQL JSONB 欄位
                )
                db.add(new_record)
            
            db.commit() # 正式寫入資料庫
            return {"ok":True}

        except Exception as e:
            db.rollback() # 出錯時回滾，保護資料
            return {"status": "error", "message": f"儲存失敗: {str(e)}"}
        finally:
            db.close() # 務必關閉資料庫連線

    else:
        db.close()
        return {
            "status": "error",
            "message": "在當前限制下找不到可行解",
        }
    
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
        results = db.query(finalscheduletable.name,finalscheduletable.schedule_data).filter(finalscheduletable.year_month == date,finalscheduletable.ward == ward).all()
        formatted_data = []
        for row in results:
            formatted_data.append({
                "schedule_date": row.name,
                "full_name": row.schedule_data,
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

