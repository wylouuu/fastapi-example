from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def voting(vote: schemas.Vote, db: Session = Depends(database.get_db), user_data: int = Depends(oauth2.get_current_user)):
    
    if vote.dir == 1:
        voted = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_data.id).first()
        
        if voted:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"user {user_data.id} has already voted on post {vote.post_id}"
            )
            
        new_vote = models.Vote(user_id = user_data.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
    
        return {
            "detail": f"Post with id: {vote.post_id} has been added"
        }
            
    else:
        voted_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_data.id)
        voted = voted_query.first()
        
        if not voted:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Post with id: {vote.post_id} was not found"
            )
            
        voted_query.delete(synchronize_session=False)
        db.commit()
    
        return {
            "detail": f"Post with id: {vote.post_id} has been deleted"
        }