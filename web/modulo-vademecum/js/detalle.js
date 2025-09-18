const params = new URLSearchParams(window.location.search);
const id = parseInt(params.get("id"));
const API_URL = "http://localhost:8200/api/v1/vademecum/1";

fetch(API_URL)
  .then(res => res.json())
  .then(data => {
    const med = data.data.find(m => m.id_medicamento === id);
    const container = document.getElementById("detalle-container");

    if (med) {
      container.innerHTML = `
        <div class="card shadow-lg p-4">
          <div class="row g-4">
            <div class="col-md-4 text-center">
              <img src="img/medicamentos/${med.id_medicamento}.jpg" class="img-fluid rounded" alt="${med.nombre_comercial}">
              <hr>
              <img src="img/laboratorios/${med.id_empresa}.png" class="img-fluid" alt="${med.nombre_laboratorio}">
            </div>
            <div class="col-md-8">
              <h2>${med.nombre_comercial}</h2>
              <h5 class="text-muted">${med.nombre_generico}</h5>
              <ul class="list-group list-group-flush mt-3">
                <li class="list-group-item"><strong>Laboratorio:</strong> ${med.nombre_laboratorio}</li>
                <li class="list-group-item"><strong>Forma farmacéutica:</strong> ${med.forma_farmaceutica}</li>
                <li class="list-group-item"><strong>Concentración:</strong> ${med.concentracion}</li>
                <li class="list-group-item"><strong>Categoría:</strong> ${med.nombre_categoria}</li>
                <li class="list-group-item"><strong>Estado:</strong> ${med.estado ? "Activo ✅" : "Inactivo ❌"}</li>
                <li class="list-group-item"><strong>Fecha de creación:</strong> ${new Date(med.fecha_creacion).toLocaleDateString()}</li>
              </ul>
              <div class="mt-4">
                <a href="index.html" class="btn btn-secondary">⬅ Volver al listado</a>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      container.innerHTML = `<div class="alert alert-danger">Medicamento no encontrado</div>`;
    }
  });
