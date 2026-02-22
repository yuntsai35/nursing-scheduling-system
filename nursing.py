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
import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="nursingdb"
)

print("database ready")


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
@app.get("/membership", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/membership.html", media_type="text/html")


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
                        "password": payload["password"]
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
            payload={"id":result[0],"full_name":result[1],"employee_num":result[2],"password":result[4], "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=7)}
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
@app.get("/api/staff")
async def staff(request: Request):
    try:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM staff")
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
    print(f"DEBUG: 接收到的 body -> {body}")

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
            print(f"SQL 執行失敗: {str(e)}")
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
        
        cursor=con.cursor(dictionary=True)
        cursor.execute("UPDATE member SET (full_name, role, level, ward, join_date)= %s,%s,%s,%s,%s WHERE employee_num= %s",[name,role,level,ward,joindate,staffid])
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
    


