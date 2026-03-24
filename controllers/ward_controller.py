from fastapi import * 
from fastapi.responses import JSONResponse
import jwt
from cache import r
import json

import os
from dotenv import load_dotenv
load_dotenv()

#sqlalchemy
from models import engine, Base, scheduled_member, settingtime, staff_number_schedule,finalscheduletable,member,ward,member_ward, SessionLocal
from .auth import check_signedin


router = APIRouter(tags=["Ward Management"])

#新增病房群組
@router.post("/api/ward")
async def insertward(request: Request, body: dict = Body(...)):
    db=SessionLocal()
    id = check_signedin(request)
    
    ward_name=body["ward_name"]

    try:
        new_ward = ward(ward_name=ward_name)
        db.add(new_ward)
        db.flush()
        combine=member_ward(staff_id=id,ward_id=new_ward.id,role='Head_Nurse')
        db.add(combine)
        db.commit()

        cache_key = f"member_list:member_id:{id}"
        r.delete(cache_key)
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


@router.delete("/api/member_ward")
async def deletemember_ward(request:Request, body: dict = Body(...)):
    db=SessionLocal()
    id = check_signedin(request)

    
    ward_id=body["ward_id"]
    results=db.query(member_ward.role).filter(member_ward.ward_id == ward_id,member_ward.staff_id==id, member_ward.role == 'Head_Nurse')
    if not results:
            return JSONResponse(status_code=403, content={"error": True, "message": "只有該病房的護理長可以刪除整個群組"})

    try:
        db.query(member_ward).filter(member_ward.ward_id == ward_id).delete()
        db.query(settingtime).filter(settingtime.ward_id == ward_id).delete()
        db.query(scheduled_member).filter(scheduled_member.ward_id == ward_id).delete()
        db.query(staff_number_schedule).filter(staff_number_schedule.ward_id == ward_id).delete()
        db.query(finalscheduletable).filter(finalscheduletable.ward_id == ward_id).delete()
        db.query(ward).filter(ward.id == ward_id).delete()
        db.commit()
        
        cache_key = f"member_list:member_id:{id}"
        r.delete(cache_key)
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
@router.get("/api/ward/{ward_id}/staff")
async def get_staff_list(request: Request, ward_id: int = None):
    cache_key = f"member_list:ward:{ward_id}"

    cached_data = r.get(cache_key)
    if cached_data:
        return {"data": json.loads(cached_data),"source": "redis"}
    
    
    
    db=SessionLocal()
    id = check_signedin(request)

    try:
        results = db.query(member, member_ward.role, member_ward.level,ward.ward_name).join(member_ward, member.id == member_ward.staff_id).join(ward, member_ward.ward_id == ward.id).filter(member_ward.ward_id == ward_id).order_by(member.employee_num.asc()).all()

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

#不在本群組內
@router.get("/api/ward/{ward_id}/staffexcept")
async def get_staff_list(request: Request,ward_id: int):    
    db=SessionLocal()
    id = check_signedin(request)

    try:
        all_staff_query = db.query(member)

        in_ward_query = db.query(member).join(member_ward, member.id == member_ward.staff_id).filter(member_ward.ward_id == ward_id)

        results = all_staff_query.except_(in_ward_query).order_by(member.employee_num.asc()).all()

        data_list = []
        for user in results:
            data_list.append({
                "id": user.id,
                "employee_num": user.employee_num,
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
    
         
@router.post("/api/ward/{ward_id}/staff")
async def insertstaff(request: Request,ward_id: int, body: dict = Body(...)):
    db=SessionLocal()
    id = check_signedin(request)
    
    staffid=body["staffid"]
    level=body["level"]


    if level == "無職級":
         level= None

    if not all([staffid,level,ward_id]):
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "建立失敗，輸入不正確或其他原因"}
            )

    try:
        existing_relation = db.query(member_ward).filter(
            member_ward.staff_id == staffid, 
            member_ward.ward_id == ward_id
        ).first()

        if existing_relation:
            return JSONResponse(status_code=400, content={"error": True, "message": "此人員已在該病房群組中"})

        if level == "none" or level == "無職級":
            level = None

        new_relation = member_ward(
            staff_id=staffid,
            ward_id=ward_id,
            role="Staff_Nurse",
            level=level)
        
        db.add(new_relation)
        db.commit()

        cache_key = f"member_list:ward:{ward_id}"
        r.delete(cache_key)
        
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
         

    
@router.delete("/api/ward/{ward_id}/staff")
async def deletestaff(request:Request,ward_id: int, body: dict = Body(...)):
    db=SessionLocal()
    id = check_signedin(request)
    
    staffid=body["staffid"]

    try:
        target = db.query(member_ward).filter(member_ward.ward_id == ward_id, member_ward.staff_id == staffid).first()
        db.delete(target)
        db.commit()
        
        cache_key = f"member_list:ward:{ward_id}"
        r.delete(cache_key)

        return {"ok":True}
        
    except jwt.PyJWTError: 
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    finally:
         db.close()
    

@router.patch("/api/ward/{ward_id}/staff")
async def editstaff(request:Request,ward_id: int, body: dict = Body(...)):
    db=SessionLocal()
    id = check_signedin(request)
        
    try:
        staffid=body["staffid"]
        level=body["level"]
        if level == "無職級":
             level = None
        
        target = db.query(member_ward).filter(member_ward.ward_id == ward_id, member_ward.staff_id == staffid).first()
        if level == "none" or level == "無職級":
            target.level = None
        else:
            target.level = level
        db.commit()

        cache_key = f"member_list:ward:{ward_id}"
        r.delete(cache_key)
        
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
    