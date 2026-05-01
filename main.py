from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import models, schemas
from database import engine, SessionLocal
from utils import hash_password, verify_password
from auth import create_token, verify_token

# 🔧 Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  Serve Frontend
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


#  REGISTER
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered"}


#  LOGIN
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token}


# 📦 CREATE TASK
@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        completed=False,
        owner_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created"}


# 📦 GET TASKS
@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    tasks = db.query(models.Task).filter(models.Task.owner_id == user.id).all()
    return tasks


#  UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task.title
    db_task.priority = task.priority
    db_task.due_date = task.due_date

    db.commit()

    return {"message": "Task updated"}


# ✔️ TOGGLE COMPLETE
@app.patch("/tasks/{task_id}/complete")
def toggle_complete(
    task_id: int,
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    db.commit()

    return {"message": "Task updated"}


# ❌ DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


#  ADMIN DELETE
@app.delete("/admin/tasks/{task_id}")
def admin_delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_email: str = Depends(verify_token)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Admin deleted task"}
