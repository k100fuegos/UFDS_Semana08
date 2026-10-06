import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

IMAGENES_DIRECCION = Path(__file__).resolve().parent.parent / "imagenes"
TIPOS_PERMITIDOS = {
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
}


def guardar_imagen(archivo: UploadFile) -> dict[str, str]:
    extension = Path(archivo.filename or "").suffix.lower()
    extensiones_permitidas = TIPOS_PERMITIDOS.get(archivo.content_type or "")
    if extensiones_permitidas is None or extension not in extensiones_permitidas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido. Solo se permiten imágenes JPEG y PNG.",
        )

    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    direccion_archivo = IMAGENES_DIRECCION / nombre_archivo
    IMAGENES_DIRECCION.mkdir(parents=True, exist_ok=True)

    with direccion_archivo.open("wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    return {
        "nombre": nombre_archivo,
        "tipo": archivo.content_type or "",
        "url": f"/imagenes/{nombre_archivo}",
    }
