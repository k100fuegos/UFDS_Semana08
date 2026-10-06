from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from config.security_Dependencia import Token_Dependencia
from services.guardar_imagen import guardar_imagen

router = APIRouter(prefix="/productos")


@router.post("/imagen")
def subir_imagen(
    imagen: Annotated[UploadFile, File(...)],
    token: Token_Dependencia,
):
    if token["id_rol"] != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
        )

    return guardar_imagen(imagen)
