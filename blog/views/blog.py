from sqlalchemy.orm import Session
from .. import models, schemas

from fastapi import Depends, HTTPException, status

from .. import database
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)


def get_all(db: Session, user_id: int):
    cache_key = f"user_{user_id}"

    cached_response = cache.get(cache_key)
    if cached_response:
        print("cached_response==>",cached_response)
        return cached_response

    blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id).all()
    cache[cache_key] = blogs
    return blogs


def create(request: schemas.Blog, db: Session, user_id: int):
    new_blog = models.Blog(title=request.title,
                           body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"id": new_blog.id}


def destroy(id: int, db: Session, user_id: int):
    blog = db.query(models.Blog).filter(
        models.Blog.id == id, models.Blog.user_id == user_id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'




def show(id: int, db: Session, user_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id,
                                        models.Blog.user_id == user_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog
