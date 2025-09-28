from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.direccion import create_direccion, get_direccion, update_direccion
from database import get_db
from schemas.direccion import DireccionCreate, DireccionUpdate

router = APIRouter(prefix="/direccion", tags=["Dirección"])
templates = Jinja2Templates(directory="templates")

@router.get("/{direccion_id}", response_class=HTMLResponse)
def form_editar_direccion(request: Request, direccion_id: int, db: Session = Depends(get_db)):
    direccion = get_direccion(db, direccion_id)
    return templates.TemplateResponse("direccion_form.html", {"request": request, "direccion": direccion})

@router.get("/", response_class=HTMLResponse)
def form_nueva_direccion(request: Request):
    # formulario vacío
    return templates.TemplateResponse("direccion_form.html", {"request": request, "direccion": None})

@router.post("/guardar", response_class=HTMLResponse)
def guardar_direccion(
    request: Request,
    db: Session = Depends(get_db),
    id: int = Form(None),
    calle: str = Form(...),
    numero: str = Form(None),
    complemento: str = Form(None),
    id_comuna: int = Form(None),
    id_provincia: int = Form(None),
    id_region: int = Form(None),
    codigo_postal: str = Form(None),
    latitud: float = Form(None),
    longitud: float = Form(None),
):
    data = {
        "calle": calle,
        "numero": numero,
        "complemento": complemento,
        "id_comuna": id_comuna,
        "id_provincia": id_provincia,
        "id_region": id_region,
        "codigo_postal": codigo_postal,
        "latitud": latitud,
        "longitud": longitud,
    }

    if id:  # actualizar
        updated = update_direccion(db, id, DireccionUpdate(**data))
        mensaje = "Dirección actualizada con éxito"
    else:   # crear
        updated = create_direccion(db, DireccionCreate(**data))
        mensaje = "Nueva dirección creada con éxito"

    return templates.TemplateResponse("direccion_form.html", {
        "request": request,
        "direccion": updated,
        "mensaje": mensaje
    })
