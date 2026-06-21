from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, get_db
from pydantic import BaseModel
import models, schemas, users, auth

models.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(users.User).filter(users.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    new_user = users.User(
        email=user.email,
        hashed_password=users.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Kayıt başarılı"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(users.User).filter(users.User.email == form.username).first()
    if not user or not users.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
    token = auth.create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def root():
    return {"message": "Todo API çalışıyor!"}

@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    new_todo = models.Todo(title=todo.title, description=todo.description, user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo bulunamadı")
    db.delete(todo)
    db.commit()
    return {"message": "Silindi"}