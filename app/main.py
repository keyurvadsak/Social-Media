from fastapi import FastAPI
from app import models
from app.database.database import engine
from app import models
from app.routers import auth,Post,Profile,Likes,Comments
# from fastapi import Request
# import time
# from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


models.Base.metadata.create_all(bind = engine)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_methods = ["*"], 
#     allow_headers = ["*"]   
# )

# @app.middleware("http")
# async def middleware(request:Request,call_next):
#     start = time.time()
#     response = await call_next(request)
#     end = time.time() - start
#     response.headers['X-Process-time'] = str(end)
#     return response


app.include_router(auth.router)
app.include_router(Post.router)
app.include_router(Profile.router)
app.include_router(Likes.router)
app.include_router(Comments.router)



@app.get("/")
async def read_root():
    return {"Hello": "World"}