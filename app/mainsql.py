# It has raw psycopg2 query to test the posts

from fastapi import FastAPI, status, HTTPException
import psycopg2
import psycopg2.extras
from pydantic import BaseModel

app = FastAPI()
#postgres://moivxdus:zIIBfsY8kXLQsDpf1cOLaIQnmho3cGqQ@tiny.db.elephantsql.com/moivxdus

while True:
    try:
        conn = psycopg2.connect(host = 'tiny.db.elephantsql.com', dbname='moivxdus', user='moivxdus', password = 'zIIBfsY8kXLQsDpf1cOLaIQnmho3cGqQ')
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        print("Database Connected Successfully")
        break
    except Exception as e:
        print("Database connection failure")
        print(e)

#Pydantic Schema

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True

# GET
@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    post_result = cursor.fetchall()
    if not post_result:
        raise HTTPException(status_code = status.HTTP_200_OK, detail = "No more posts in database")
    return {"data": post_result}

# POST
@app.post('/posts', status_code = status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, is_published) values(%s, %s, %s) RETURNING * """, (post.title, post.content, post.is_published))
    post_result = cursor.fetchone()
    conn.commit()
    return {"data": post_result}

# GET Detail

@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE ID = %s""", (str(id),))
    post_result = cursor.fetchone()
    if not post_result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Post {}".format(id))
    return {"data": post_result}

# PUT DETAIL

@app.put('/posts/{id}', status_code = status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.is_published, str(id)))
    conn.commit()
    post_result = cursor.fetchone()
    if not post_result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Post {id}")
    return {"data": post_result}

# DELETE DETAIL

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    conn.commit()
    post_result = cursor.fetchone()
    if not post_result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Post {id}")
    return {"data": post_result}
