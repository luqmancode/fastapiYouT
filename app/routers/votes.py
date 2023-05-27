from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(
    prefix = "/vote", tags = ['votes']
)

@router.post('/', response_model = schemas.VoteResponse)
async def create_vote(vote: schemas.VoteRequest, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_active_user)):
    to_vote_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not to_vote_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"{vote.post_id} does not exist to vote")
    vote_exist_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)
    db_vote_exist = vote_exist_query.first()
    if vote.vote_direction == 1:
        # Add Vote if vote not exists on particular user and post
        if not db_vote_exist:
            db_vote = models.Vote(post_id = vote.post_id, user_id = curr_user.id)
            db.add(db_vote)
            db.commit()
            return {"status": "Successfully voted on post {}".format(vote.post_id)}
        else:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Voting already done on {vote.post_id}")
    else:
        # Remove Vote if only vote exists on particular user and post
        if db_vote_exist:
            vote_exist_query.delete(synchronize_session = False)
            db.commit()
            return {"status": f"Successfully deleted vote on post {vote.post_id}"}
        else:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"{vote.post_id} post is not already voted to remove vote")