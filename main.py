from fastapi import FastAPI, HTTPException
from sqlalchemy import desc, select, cast, Integer
from dotenv import load_dotenv
from models.posts import post_table
from models.users import users_table
load_dotenv()
from routers import users
from routers import posts
from models.database import database
app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
@app.on_event("startup")
async def startup():
    await database.connect()
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
@app.get("/")
async def read_root():

    try:
        query = (
        select(

                post_table.c.id,
                post_table.c.created_at,
                post_table.c.title,
                post_table.c.content,
                post_table.c.user_id,
                users_table.c.name.label("user_name"),

            )
            .select_from(post_table.join(users_table,  cast(post_table.c.user_id, Integer) == users_table.c.id))
            .order_by(desc(post_table.c.created_at))
        )

        return await database.fetch_all(query)
    except Exception as e:
        print('Database error')
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

