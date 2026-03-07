from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import datetime
from datetime import timezone
import jwt

import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.getenv("DB_PASSWORD"),
  database="nursingdb"
)
print("database ready")

def check_db():
    cursor=con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS nursingdb")
    cursor.execute("USE nursingdb")
    cursor.execute("CREATE TABLE IF NOT EXISTS `staff` ( `id` int NOT NULL AUTO_INCREMENT,`full_name` varchar(50) NOT NULL,`employee_num` varchar(20) NOT NULL,`password` varchar(255) NOT NULL,`role` enum('IT_Admin','Head_Nurse','Staff_Nurse') NOT NULL,`level` enum('N0','N1','N2','N3','N4') DEFAULT NULL,`ward` varchar(20) DEFAULT NULL,`join_date` datetime DEFAULT CURRENT_TIMESTAMP,`is_temp_password` tinyint(1) DEFAULT '1',PRIMARY KEY (`id`),UNIQUE KEY `employee_num` (`employee_num`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
    cursor.execute("SELECT COUNT(*) FROM staff WHERE employee_num = 'ADM0001'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO staff (full_name, employee_num, password, role, is_temp_password) VALUES ('系統管理員', 'ADM0001', 'ADM0001', 'IT_Admin', 1)")
        con.commit()
        print("Initial admin account created.")

    cursor.close()
    print("Database and table 'staff' are ready.")
check_db()

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
    
    employee_num=body["employee_num"]
    password=body["password"]

    cursor=con.cursor()
    cursor.execute("SELECT * FROM staff WHERE employee_num=%s AND password=%s",[employee_num, password])
    result=cursor.fetchone()
    cursor.close()

    try:
        if result:
            payload={"id":result[0],"full_name":result[1],"employee_num":result[2],"password":result[3],"role":result[4],"ward":result[6], "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=7)}
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

#員工管理
@app.get("/api/staff/{role}")
async def staff(request: Request, role: str = None):
    try:
        cursor=con.cursor()
        if role == 'adminstaff':
             cursor.execute("SELECT * FROM staff where role ='IT_Admin' or role = 'Head_Nurse'")
        else:
             cursor.execute("SELECT * FROM staff where role ='Staff_Nurse'")
        results = cursor.fetchall()
        cursor.close()
        
        return {"data": results}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    
         
@app.post("/api/staff")
async def insertstaff(request: Request, body: dict = Body(...)):

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
        cursor = con.cursor(dictionary=True)
        cursor.execute("INSERT INTO staff (employee_num, full_name,password, role, level, ward, join_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",[staffid,name,password,role,level,ward,joindate])
        con.commit()
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

    
@app.delete("/api/staff")
async def deletestaff(request:Request, body: dict = Body(...)):
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
        cursor = con.cursor(dictionary=True)
        cursor.execute("DELETE FROM staff WHERE id=%s",[staffid])
        con.commit() 
        cursor.close()
        return {"ok":True}
        
    except jwt.PyJWTError: 
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    

@app.patch("/api/staff")
async def editstaff(request:Request, body: dict = Body(...)):
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

        cursor=con.cursor(dictionary=True)
        cursor.execute("UPDATE staff SET full_name = %s, role = %s, level = %s, ward = %s, join_date = %s WHERE employee_num = %s",[name,role,level,ward,joindate,staffid])
        con.commit()
        cursor.close()
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
    

@app.patch("/api/settingtime")
async def updatesettingtime(request:Request, body: dict = Body(...)):
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


        cursor=con.cursor(dictionary=True)
        cursor.execute("UPDATE settingtime SET min_shift_interval=%s,min_rest_2w=%s,min_rest_1m=%s,max_hours_1w=%s,max_hours_1d=%s,max_continuous_work=%s,max_shifts_1w=%s WHERE ward = %s",[ min_shift_interval, min_rest_2w, min_rest_1m, max_hours_1w, max_hours_1d, max_continuous_work, max_shifts_1w, ward])
        con.commit()
        cursor.close()
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

@app.get("/api/settingtime")
async def savesettingtime(request: Request):
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
        cursor=con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM settingtime where ward =%s",[ward])
        result = cursor.fetchone()
        cursor.close()

        return {"data":result}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    
@app.get("/api/settingmember")
async def savesettingtime(request: Request):
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
        cursor=con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM settingtime where ward =%s",[ward])
        result = cursor.fetchone()
        cursor.close()

        return {"data":result}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    
@app.get("/api/staff")
async def staff(request: Request):
    try:
        cursor=con.cursor()
        cursor.execute("SELECT id, full_name FROM staff where role ='Staff_Nurse'")
        results = cursor.fetchall()
        cursor.close()
        
        return {"data": results}
    except HTTPException:
            raise HTTPException(
				status_code=500,
				detail={
					"error": True,
					"message": "請依照情境提供對應的錯誤訊息"
				}
			)
    
@app.post("/api/settingmember")
async def updatesettingmember(request:Request, body: dict = Body(...)):
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

        cursor=con.cursor()
        cursor.execute("DELETE FROM scheduled_member WHERE schedule_id = %s and ward =%s",[schedule_id, ward])

        for id in staff_id:
             cursor.execute("INSERT INTO scheduled_member (schedule_id, staff_id, schedule_date,ward) VALUES (%s, %s, %s, %s)",[schedule_id,id,schedule_date,ward])
        
        con.commit()
        cursor.close()
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
    
#目前為固定的版本，請修改成彈性可增加項目的樣子
@app.post("/api/settingstaffnumber")
async def insertsettingstaffnumber(request:Request, body: dict = Body(...)):
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

        cursor=con.cursor()
        cursor.execute("DELETE FROM  staff_number_schedule WHERE ward =%s",[ward])


        shifting_group=[("day",required_dayshift,"",ward),("night",required_nightshift,selectedNightStaff,ward),("midnight", required_mignightshift, selectedMidnightStaff,ward)]

        for data in shifting_group:     
           cursor.execute("INSERT INTO staff_number_schedule (shift, shift_staff_number, staff_id, ward) VALUES (%s, %s, %s, %s)",data)
        
        con.commit()
        cursor.close()
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
