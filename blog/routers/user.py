from fastapi import APIRouter,Depends,status,HTTPException,Response
from typing import List
from sqlalchemy.orm import Session

from .. import schemas,database,models
from ..hashing import Hash
from ..views import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)

  