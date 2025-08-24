from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.schemas.dashboard_inicial import DashboardInicialCreate, DashboardInicialUpdate, DashboardInicialOut

router = APIRouter(prefix="/dashboard", tags=["DashboardInicial"])

@router.get("/", response_model=list[DashboardInicialOut])
def read_dashboards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.dashboard_inicial.get_dashboards(db, skip=skip, limit=limit)

@router.get("/{dashboard_id}", response_model=DashboardInicialOut)
def read_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    db_dashboard = crud.dashboard_inicial.get_dashboard(db, dashboard_id)
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard no encontrado")
    return db_dashboard

@router.post("/", response_model=DashboardInicialOut)
def create_dashboard(dashboard: DashboardInicialCreate, db: Session = Depends(get_db)):
    return crud.dashboard_inicial.create_dashboard(db, dashboard)

@router.put("/{dashboard_id}", response_model=DashboardInicialOut)
def update_dashboard(dashboard_id: int, dashboard: DashboardInicialUpdate, db: Session = Depends(get_db)):
    db_dashboard = crud.dashboard_inicial.update_dashboard(db, dashboard_id, dashboard)
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard no encontrado")
    return db_dashboard

@router.delete("/{dashboard_id}")
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    success = crud.dashboard_inicial.delete_dashboard(db, dashboard_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dashboard no encontrado")
    return {"detail": "Dashboard eliminado correctamente"}
