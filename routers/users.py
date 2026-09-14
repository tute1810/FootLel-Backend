from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    return [{"id": 1, "nombre": "Matías"}, {"id": 2, "nombre": "Admin"}]