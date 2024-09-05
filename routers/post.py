from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import Session, ENGINE
from models import Post, User
from schemas import PostCreate, PostUpdateModel
from fastapi_jwt_auth import AuthJWT




Session = Session(bind=ENGINE)
post_router = APIRouter(prefix="/posts", tags=["posts"])

@post_router.get("/")
async def post():
    posts = Session.query(Post).all()
    try:
        if posts:
            return jsonable_encoder({
                'status': 'success',
                'posts': posts
            })
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

@post_router.get('/one-person')
async def one_person(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            posts = Session.query(Post).filter(Post.user == check_user).all()
            data = {
                "status": 200,
                "message": f"posts created by {Authorize.get_jwt_subject()}",
                "posts" : jsonable_encoder(posts)
            }
            return data
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials or post not found")


@post_router.post("/create")
async def post(post: PostCreate, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            new_post = Post(
                image_path=post.image_path,
                caption=post.caption,
            )
            Session.add(new_post)
            Session.commit()
            data = {
                "status": 201,
                "message": "post created",
                "detail" :{
                    "user": Authorize.get_jwt_subject(),
                    "image_path": new_post.image_path,
                    "caption": new_post.caption,
                    "created_at": new_post.created_at
                }
            }
            return jsonable_encoder(data)

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')

@post_router.put("/update/{post_id}")
async def update_post(post_id: str, post: PostUpdateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if not check_user:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        post_to_update = Session.query(Post).filter(Post.id == post_id, Post.user_id == check_user.id).first()
        if not post_to_update:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


        for key, value in post.dict(exclude_none=True).items():
            setattr(post_to_update, key, value)

        Session.commit()

        return jsonable_encoder({
            "status": 200,
            "message": "Post updated",
            "detail": {
                "user": Authorize.get_jwt_subject(),
                "post": post_to_update
            }
        })

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')



@post_router.delete("/delete/{post_id}")
async def delete_post(post_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if not check_user:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        post_to_delete = Session.query(Post).filter(Post.id == post_id, Post.user_id == check_user.id).first()
        if not post_to_delete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        Session.delete(post_to_delete)
        Session.commit()

        return jsonable_encoder({
            "status": 200,
            "message": "Post deleted",
        })

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')
