# posts
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts", tags = ['posts']
)

# GET ALL
@router.get('/', response_model = List[schemas.PostResponse]) # curr_user: int = Depends(oauth2.get_active_user),
# @router.get('/', response_model = List[schemas.PostVoteResponse])
async def get_posts(db: Session = Depends(database.get_db),  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    post_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    # post_query = db.query(models.Post).filter(models.Post.user_id == curr_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    # print(2222, curr_user.email)
    # post_query = db.query(models.Post, func.count(models.Vote.post_id).label("vote_counts")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    # print(1111, post_query)
    post_result = post_query.all()
    if not post_result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No more posts available")
    # return {"data": post_result}
    # print(2222, post_result)
    return post_result

# GET ONE ANY USER CONTENT DETAIL VIEW
@router.get('/{id}', response_model = schemas.PostResponseDetail)
async def get_post(id: int, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_active_user)):
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    print(22222222, post_query)
    print(33333333, curr_user.email)
    db_post = post_query.first()
    if not db_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(str(id)))
    # return {"data": db_post} after Response Model
    return db_post

# POST
@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponseDetail)
async def create_post(post: schemas.PostRequest, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_active_user)):
    current_user_id = curr_user.id
    db_post = models.Post(user_id = current_user_id, **post.dict())
    # db_post = models.Post(title = post.title, content = post.content, is_published = post.is_published)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # return {"data": db_post}
    return db_post

# PATCH 
@router.patch('/{id}', response_model = schemas.PostResponse)
async def patch_post(id: int, post: schemas.PostRequest, db: Session = Depends(database.get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == str(id)).first()
    if not db_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(str(id)))
    db_post.title = post.title
    db_post.content = post.content
    db_post.is_published = post.is_published
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # return {"data": db_post}
    return db_post

# PUT
@router.put('/{id}', response_model = schemas.PostResponseDetail)
async def update_post(id: int, post: schemas.PostRequest, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_active_user)):
    db_query = db.query(models.Post).filter(models.Post.id == id)
    if not db_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(str(id)))
    else:
        db_post = db_query.first()
        print(999, db_post.user_id, type(db_post.user_id), curr_user.id, type(curr_user.id))
        if db_post.user_id != curr_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not having priviledged to perform this request")
    db_query.update(post.dict(), synchronize_session = False)
    db.commit()
    # return {"data": db_query.first()}
    return db_query.first()

# DELETE
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_active_user)):
    # db_post = db.query(models.Post).filter(models.Post.id == str(id)).first()
    # if not db_post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(str(id)))
    # db.delete(db_post)
    # db.commit()

    db_query = db.query(models.Post).filter(models.Post.id == str(id))
    print(444, db_query, type(db_query), type(db_query.first()), db_query.first())
    if not db_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(str(id)))
    else:
        db_post  = db_query.first()
        if db_post.user_id != curr_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not allowed to delete this resource")
    db_query.delete(synchronize_session = False)
    db.commit()