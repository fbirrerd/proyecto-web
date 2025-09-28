from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.app.schemas.respond import objRespuesta
from app.database import get_db
from app.schemas import dashboard_inicial
from app.schemas.dashboard_inicial import (
    DashboardInicialCreate,
    DashboardInicialUpdate,
    DashboardInicialOut,
)
from app.services.dashboard_inicial import (
    get_dashboard,
    get_dashboards,
    create_dashboard as create_dashboard_service,
    update_dashboard as update_dashboard_service,
    delete_dashboard as delete_dashboard_service
)

router = APIRouter(prefix="/dashboard", tags=["DashboardInicial"])


@router.get("/", response_model=list[DashboardInicialOut])
def read_dashboards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = get_dashboards(db, skip=skip, limit=limit)
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registro: {str(e)}"
        )


@router.get("/{dashboard_id}", response_model=DashboardInicialOut)
def read_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    try:
        data = get_dashboard(db, dashboard_id)
        if datos is None:
            raise HTTPException(status_code=404, detail="Escritorio no encontrado")
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registro: {str(e)}"
        )

@router.post("/", response_model=DashboardInicialOut)
def create_dashboard(dashboard: DashboardInicialCreate, db: Session = Depends(get_db)):
    try:
        data = create_dashboard_service(db, dashboard)
        return objRespuesta(
            respuesta = True,
            data=dashboard
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )

@router.put("/{dashboard_id}", response_model=DashboardInicialOut)
def update_dashboard(dashboard_id: int, dashboard: DashboardInicialUpdate, db: Session = Depends(get_db)):
    try:
        db_dashboard = update_dashboard_service(db, dashboard_id, dashboard)
        if not db_dashboard:
            raise HTTPException(status_code=404, detail="Dashboard no encontrado")
        return db_dashboard
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )


@router.delete("/{dashboard_id}")
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_dashboard_service(db, dashboard_id)
        if not success:
            raise HTTPException(status_code=404, detail="Dashboard no encontrado")
        return {"detail": "Dashboard eliminado correctamente"}
    except SQLAlchemyError as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )
