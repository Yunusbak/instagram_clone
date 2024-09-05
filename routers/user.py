from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from models import User
from database import Session, ENGINE

Session = Session(bind=ENGINE)

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get('/')
async def get_users(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        users = Session.query(User).all()
        data = {
            "status": 200,
            "message": "All users in instagram have been successfully authenticated",
            "users" : users
        }
        return jsonable_encoder(data)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")


