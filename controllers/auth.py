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
from models import member,ward,member_ward, SessionLocal


from datetime import datetime
from decimal import Decimal



router = APIRouter(tags=["Authentication"])



def check_signedin(request: Request):
    bearerToken = request.headers.get("Authorization")
    if not bearerToken:
        raise HTTPException(status_code=403, detail="未登入系統，拒絕存取")

    try:
        token = bearerToken.split(" ")[1]
        payload = jwt.decode(token, os.getenv("SECRET_PASSWORD"), algorithms=["HS256"])
        return payload["id"]
    except Exception:
        raise HTTPException(status_code=403, detail="憑證無效")


#會員
@router.post("/api/user/auth")
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


@router.get("/api/user/auth")
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

@router.put("/api/user/auth")
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



#快取ward資料 為了驗證
@router.get("/api/member_ward")
async def get_ward_list(request: Request):
    db=SessionLocal()
    id = check_signedin(request)

    cache_key = f"member_list:member_id:{id}"

    cached_data = r.get(cache_key)
    if cached_data:
        return {"data": json.loads(cached_data),"source": "redis"}
        

    try:
        result=db.query(member_ward.role,member_ward.ward_id,ward.ward_name).join(ward, member_ward.ward_id == ward.id).filter(member_ward.staff_id == id).all()
        data_list = []
        for row in result:
            data_list.append({
                "role": row.role,
                "ward_id": row.ward_id,
                "ward_name":row.ward_name
            })

        r.setex(cache_key, 3600, json.dumps(data_list))

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


    
#會員姓名及修改
@router.get("/api/memberinfo")
async def getmembership(request: Request):
    db = SessionLocal()  
    current_user_id = check_signedin(request)

    try:

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
@router.patch("/api/membership")
async def updatemembership(request: Request, body: dict = Body(...)):
    db = SessionLocal()
    current_user_id = check_signedin(request)
    try:
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
