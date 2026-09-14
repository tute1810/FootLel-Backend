from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{user_id}")
def endpoint_obtener_usuario(user_id: int):
    #resultado = get_user(user_id) 
    
    return None 