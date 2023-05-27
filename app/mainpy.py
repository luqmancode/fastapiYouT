from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random 


app = FastAPI()

@app.get('/posts')
async def get_posts():
    return {"data": post_data}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

post_data = [{"id": 1, "title": "First Title", "content": "First Content"}, {"id": 2, "title": "Second Title", "content": "Second Content"}]

@app.post('/posts')
async def create_posts(post: Post, response: Response):
    post_dict = post.dict()
    post_dict['id'] = random.randint(3, 10000)
    post_data.append(post_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"data": post_dict}

@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    for post in post_data:
        if post['id'] == id:
            response.status_code = status.HTTP_200_OK
            return {"data": post}
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post Id")
    
@app.put('/posts/{id}')
async def update_post(id: int, new_post: Post, response: Response):
    for i, post in enumerate(post_data):
        if post['id'] == id:
            post_data[i] = new_post
            response.status_code = status.HTTP_202_ACCEPTED
            return {"data": new_post}
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post Id")
    
@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    popped_item = None
    for i, p in enumerate(post_data):
        if p['id'] == id:
            popped_item = post_data.pop(i)
    if not popped_item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post Id")
