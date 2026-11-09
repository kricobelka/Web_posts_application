from itertools import count

from fastapi import FastAPI
from models.post import Post
from fastapi import FastAPI, HTTPException
from models.post import Post, UpdatePost, PatchPost, CreatePost

# Создаем само приложение, которое ищет Uvicorn (переменная app)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

posts = []
post_id = count(1)
post_not_exist_message = "Post not found"

@app.get("/posts")
def get_posts():
    return {"posts": posts}

@app.get("/posts/{post_id}",
         responses={404: {"desctiption": post_not_exist_message}})
def get_post_by_id(post_id: int):
    for post in posts:
        if post.id == post_id:
            return {"post_topic": post.topic, "post_body": post.body}
        
    raise HTTPException(
        status_code=404,
        detail=post_not_exist_message
    )

@app.post("/posts")
def create_post(post: CreatePost):

    new_post = Post(
        id= next(post_id),
        topic=post.topic,
        body=post.body
    )

    posts.append(new_post)
    return {"message": "Post has been created",
            "post": new_post}


@app.put("/posts/{post_id}",
         responses={404: {"description": post_not_exist_message}})
def update_post(post_id: int, post_data: UpdatePost):
    for post in posts:
        if post.id == post_id:
            post.topic = post_data.topic
            post.body = post_data.body
            return {"message": "Post has been updated"}

    raise HTTPException (
        status_code=404,
        detail=post_not_exist_message
    )

@app.patch("/posts/{post_id}",
           responses = {404: {"description": post_not_exist_message}})
def update_topic_post(post_id: int, post_data: PatchPost):
    for post in posts:
        if post.id == post_id:
            updated_data = post_data.model_dump(exclude_unset=True)

            if not updated_data:
                raise HTTPException(
                    status_code=400,
                    detail="No fields for update"
                )
            
            # first way:
            # if "topic" in updated_data:
            #     post.topic = updated_data["topic"]

            # if "body" in updated_data:
            #     post.body = updated_data["body"]

            # 2nd way:
            for key, value in updated_data.items():
                setattr(post, key, value)
                
            return {"message": "Post has been updated",
                    "updated_post": {
                        "id": post.id,
                        "topic": post.topic,
                        "body": post.body
                    }
            }

    raise HTTPException (
            status_code=404,
            detail=post_not_exist_message
        )

@app.delete("/posts/{post_id}",
            responses = {404: {"description": post_not_exist_message}})
def delete_post(post_id: int):
    for post in posts:
        if post.id == post_id:
            posts.remove(post)
            return {"message": "Post has been removed"}
        
    raise HTTPException (
                status_code=404,
                detail=post_not_exist_message
            )