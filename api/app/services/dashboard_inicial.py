from sqlalchemy.orm import Session

from app.models.models import DashboardInicial
from app.schemas.dashboard_inicial import DashboardInicialCreate, DashboardInicialUpdate

def get_dashboards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DashboardInicial).offset(skip).limit(limit).all()

def get_dashboard(db: Session, dashboard_id: int):
    return db.query(DashboardInicial).filter(DashboardInicial.id == dashboard_id).first()

def get_dashboard_pagina(db: Session, dashboard_id: int):
    objeto = db.query(DashboardInicial).filter(DashboardInicial.id == dashboard_id).first()
    if objeto:
        return objeto.pagina


def create_dashboard(db: Session, dashboard: DashboardInicialCreate):
    db_dashboard = DashboardInicial(**dashboard.dict())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

def update_dashboard(db: Session, dashboard_id: int, dashboard: DashboardInicialUpdate):
    db_dashboard = db.query(DashboardInicial).filter(DashboardInicial.id == dashboard_id).first()
    if not db_dashboard:
        return None
    update_data = dashboard.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dashboard, key, value)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

def delete_dashboard(db: Session, dashboard_id: int):
    db_dashboard = db.query(DashboardInicial).filter(DashboardInicial.id == dashboard_id).first()
    if db_dashboard:
        db.delete(db_dashboard)
        db.commit()
        return True
    return False
