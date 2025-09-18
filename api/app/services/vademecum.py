from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Imagen, VademecumCategoriaTerapeutica, VademecumLaboratorio, VademecumMedicamento, VademecumMedicamentoCategoria
from sqlalchemy.orm import aliased
from sqlalchemy import select

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import (
    Imagen,
    VademecumCategoriaTerapeutica,
    VademecumLaboratorio,
    VademecumMedicamento,
    VademecumMedicamentoCategoria,
)

from sqlalchemy.orm import Session
from app.models.models import (
    VademecumCategoriaTerapeutica,
    VademecumLaboratorio,
    VademecumMedicamento,
    VademecumMedicamentoCategoria,
)

def get_vademecum(db, id_empresa): 
    query = (
        db.query(
            VademecumMedicamento.id_medicamento,
            VademecumMedicamento.id_empresa,
            VademecumLaboratorio.nombre_laboratorio,
            VademecumMedicamento.nombre_comercial,
            VademecumMedicamento.nombre_generico,
            VademecumMedicamento.forma_farmaceutica,
            VademecumMedicamento.concentracion,
            VademecumCategoriaTerapeutica.nombre_categoria,
            VademecumMedicamento.estado,
            VademecumMedicamento.fecha_creacion,
        )
        .join(
            VademecumLaboratorio,
            (VademecumMedicamento.id_laboratorio == VademecumLaboratorio.id_laboratorio)
            & (VademecumMedicamento.id_empresa == VademecumLaboratorio.id_empresa),
        )
        .join(
            VademecumMedicamentoCategoria,
            VademecumMedicamento.id_medicamento == VademecumMedicamentoCategoria.id_medicamento,
        )
        .join(
            VademecumCategoriaTerapeutica,
            VademecumMedicamentoCategoria.id_categoria == VademecumCategoriaTerapeutica.id_categoria,
        )
        .filter(VademecumMedicamento.id_empresa == id_empresa)
        .order_by(VademecumMedicamento.nombre_comercial.asc())
    )

    return db.execute(query).mappings().all()  # 🔹 devuelve dicts, no tuplas
