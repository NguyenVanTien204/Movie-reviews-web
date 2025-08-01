from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.config import get_db
from typing import List

from schema.review import UserComment as CommentSchema, UserRating as RatingSchema
from service.user_service import RatingService, CommentService
from models.user import Comment

router = APIRouter()

@router.get("/allcomment/{movie_id}", response_model=List[CommentSchema])
async def get_all_comment(movie_id: int, db: Session = Depends(get_db)):
    orm_comments = db.query(Comment).all()
    return [CommentSchema.model_validate(comment, from_attributes=True) for comment in orm_comments]

@router.post("/user/rating", response_model= RatingSchema)
async def rate_movie(user_id: int, movie_id: int, score: float, db: Session = Depends(get_db)):
    return await RatingService.AddOrUpdateRating(user_id, movie_id, score, db)

@router.post("/user/comment", response_model= CommentSchema)
async def comment(user_id: int, movie_id: int, body: str, db: Session = Depends(get_db)):
    return await CommentService.AddOrUpdateComment(user_id, movie_id, body, db)

@router.post("/user/delete/comment", response_model= bool)
async def delete_comment(id, user_id: int, db: Session = Depends(get_db)):
    return await CommentService.delete_comment(id, user_id, db)
