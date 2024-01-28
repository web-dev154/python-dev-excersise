from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2
from ..views import blog


router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db, current_user.id)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if len(str(request.json())) > 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Payload size exceeds 1 MB",
        )
    print("len(str(request.json()))", len(str(request.json())))
    return blog.create(request, db, current_user.id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db, current_user.id)


@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db), status_code=200, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db, current_user.id)
