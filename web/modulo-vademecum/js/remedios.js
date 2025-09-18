// URL de la API
const API_URL = "http://localhost:8200/api/v1/vademecum/1";

// Estado actual de medicamentos
let medicamentosData = [];

// Cargar medicamentos desde la API
fetch(API_URL)
  .then(res => res.json())
  .then(data => {
    medicamentosData = data.data;
    renderMedicamentos(medicamentosData);
  })
  .catch(err => console.error("Error cargando medicamentos:", err));

/**
 * Renderiza medicamentos en la tabla
 */
function renderMedicamentos(meds) {
  const tbody = document.getElementById("medicamentos-list");
  tbody.innerHTML = "";

  meds.forEach(med => {
    const row = `
      <tr>
        <td><img src="img/medicamentos/${med.id_medicamento}.jpg" alt="${med.nombre_comercial}" class="img-thumbnail" style="max-width:60px;"></td>
        <td>${med.nombre_comercial}</td>
        <td>${med.nombre_generico}</td>
        <td><span class="badge bg-primary">${med.nombre_categoria}</span></td>
        <td>${med.nombre_laboratorio}</td>
        <td>
          <a href="detalle.html?id=${med.id_medicamento}" class="btn btn-sm btn-outline-primary">Ver detalle</a>
        </td>
      </tr>
    `;
    tbody.innerHTML += row;
  });
}

/**
 * Buscador en tiempo real
 */
document.getElementById("search").addEventListener("input", function () {
  const term = this.value.toLowerCase();

  const filtered = medicamentosData.filter(med =>
    med.nombre_comercial.toLowerCase().includes(term) ||
    med.nombre_generico.toLowerCase().includes(term) ||
    med.nombre_laboratorio.toLowerCase().includes(term) ||
    med.nombre_categoria.toLowerCase().includes(term)
  );

  renderMedicamentos(filtered);
});
