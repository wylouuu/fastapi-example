# -------------------------- API Library -------------------------- 

from fastapi import FastAPI
from .database import engine
from .routers import post, user, auth, vote
from .config import settings 
from fastapi.middleware.cors import CORSMiddleware

# -------------------------- API Library -------------------------- 

# -------------------------- API Apps -------------------------- 

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------- API Apps -------------------------- 

# -------------------------- API Router -------------------------- 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to my api"
    }
    
# -------------------------- API Router -------------------------- 