import json
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
    # posts = conn.execute("""SELECT * FROM posts""").fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
@router.get("/")
async def get_posts(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):    
    posts =  db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Convert SQLAlchemy objects to a format that can be serialized to JSON
    post_list = []
    for post, vote_count in posts:
        post_dict = {"post": jsonable_encoder(post), "vote_count": vote_count}
        post_list.append(post_dict)

    return post_list

    # post_by_id = conn.execute("""SELECT * FROM posts WHERE id = %s """, [str(id)]).fetchone()
@router.get("/{id}")
async def get_post_by_id(id: int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    post_by_id = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post_by_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} was not found"
        )
        
    post, vote_count = post_by_id
    post_dict = {"post": jsonable_encoder(post), "vote_count": vote_count}

    return post_dict
    
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    # new_post = conn.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", [post.title, post.content, post.published]).fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id = user_data.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    
@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    # updated_post = conn.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", [post.title, post.content, post.published, str(id)]).fetchone()
    # conn.commit()
    
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = updated_post_query.first()
    
    if updated_post == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {id} was not found"
        )
        
    if updated_post.owner_id != int(user_data.id):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"Not authorized to perform requested action"
        )
        
    updated_post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()
    
    return updated_post
    
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    # delete_post = conn.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [str(id)]).fetchone()
    # conn.commit()
    
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    deleted_post = delete_post_query.first()
    
    if deleted_post == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {id} was not found"
        )
        
    if deleted_post.owner_id != int(user_data.id):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"Not authorized to perform requested action"
        )
        
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    