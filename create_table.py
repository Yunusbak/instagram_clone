from database import Base, ENGINE
from models import User, Post, Comments, Likes, Followers, PostTags, Messages


Base.metadata.create_all(bind=ENGINE)