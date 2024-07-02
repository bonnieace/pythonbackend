# app/main.py
from fastapi import FastAPI
from app.routers import auth, entries, summary, users

app = FastAPI()

# Including the routers from different modules
app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(summary.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Journal App!"}
