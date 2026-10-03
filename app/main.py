from fastapi import FastAPI

from app.database import Base, engine
from app.routes import auth, students

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Student Records API",
    description="A secure REST API for managing student records."
)

app.include_router(auth.router)
app.include_router(students.router)


@app.get("/")
def home():
    return {
        "message": "Secure Student Records API is running!"
    }