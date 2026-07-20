from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserOut
from app.core.deps import get_current_user



router = APIRouter(prefix="/user", tags=["User"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# GET PROFILE
@router.get("/me", response_model=UserOut)
def get_my_profile(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

from app.schemas.user import UserChangePassword
from app.utils.hash import hash_password, verify_password

@router.post("/change-password")
def change_password(
    data: UserChangePassword,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not verify_password(data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}