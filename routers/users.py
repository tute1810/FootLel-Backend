from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/")
def create_user(nombre: str, db: Session = Depends(get_db)):
    new_user = User(nombre=nombre)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user