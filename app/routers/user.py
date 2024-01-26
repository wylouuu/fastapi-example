from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)
    
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):    
    #hash the password - user.password    
    hashed_password = utils.hash(user.password)
    
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model = schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    user_by_id = db.query(models.User).filter(models.User.id == id).first()
    
    if not user_by_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id: {id} doesn't not exist"
        )
    
    return user_by_id
    