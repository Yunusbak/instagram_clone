from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database import Session, ENGINE
from models import Likes, User
from schemas import LikeCreateModel



Session = Session(bind=ENGINE)


like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.get('/')
async def get_likes(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject())
        if check_user:
            likes = Session.query(Likes).filter(Likes.user == check_user).all()
            data = {
                "status": 200,
                "message" : f"This posts is liked by {Authorize.get_jwt_subject()}",
                "likes": likes
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization on failed')


@like_router.post('/create')
async def create_like(like : LikeCreateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject())
        if check_user:
            new_like = Likes(
                post_id=like.post_id,
            )
            Session.add(new_like)
            Session.commit()
            data = {
                "status": 201,
                "message": f"This post is liked by {Authorize.get_jwt_subject()} and {like.post_id}",
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization on failed')
