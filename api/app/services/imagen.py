from sqlalchemy.orm import Session

def get_imagenes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Imagen).offset(skip).limit(limit).all()

def get_imagen(db: Session, imagen_id: int):
    return db.query(Imagen).filter(Imagen.id_imagen == imagen_id).first()

def create_imagen(db: Session, imagen: ImagenCreate):
    db_imagen = Imagen(**imagen.dict())
    db.add(db_imagen)
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def update_imagen(db: Session, imagen_id: int, imagen: ImagenUpdate):
    db_imagen = db.query(Imagen).filter(Imagen.id_imagen == imagen_id).first()
    if not db_imagen:
        return None
    for field, value in imagen.dict(exclude_unset=True).items():
        setattr(db_imagen, field, value)
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def delete_imagen(db: Session, imagen_id: int):
    db_imagen = db.query(Imagen).filter(Imagen.id_imagen == imagen_id).first()
    if not db_imagen:
        return None
    db.delete(db_imagen)
    db.commit()
    return db_imagen
