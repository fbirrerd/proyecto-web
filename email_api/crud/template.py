from sqlalchemy.orm import Session

from schemas.template import TemplateCreate
from models.template import Template


def crear_template(db: Session, template: TemplateCreate):
    db_template = Template(
        name=template.name,
        subject=template.subject,
        body_html=template.body_html,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def obtener_template_x_id(db: Session, template_id: int):
    return db.query(Template).filter(Template.id == template_id).first()

def obtener_templates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Template).offset(skip).limit(limit).all()
