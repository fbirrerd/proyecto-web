$(document).ready(function() {
  let remedios = [];

  // Renderiza la lista de remedios
  function renderRemedios(lista) {
    $("#lista-remedios").empty();
    lista.forEach(r => {
      $("#lista-remedios").append(`
        <div class="col">
          <div class="card h-100 shadow-sm">
            <div class="row g-0">
              <div class="col-md-4 p-2">
                <img src="img/${r.foto}" class="img-fluid rounded-start" alt="${r.nombre}">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">${r.nombre}</h5>
                  <p class="card-text"><strong>Laboratorio:</strong> ${r.laboratorio}</p>
                  <p class="card-text"><strong>Ingrediente principal:</strong> ${r.ingredientes[0]}</p>
                  <p class="card-text"><strong>Precio:</strong> ${r.precio}</p>
                  <a href="detalle.html?id=${r.id}" class="btn btn-primary btn-sm">Ver detalle</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      `);
    });
  }

  // Aplica los filtros en la lista de remedios
  function aplicarFiltros() {
    const nombre = $("#filtro-nombre").val().toLowerCase();
    const lab = $("#filtro-laboratorio").val().toLowerCase();
    const ing = $("#filtro-ingrediente").val().toLowerCase();
    const via = $("#filtro-via").val().toLowerCase();

    const filtrado = remedios.filter(r =>
      r.nombre.toLowerCase().includes(nombre) &&
      r.laboratorio.toLowerCase().includes(lab) &&
      r.ingredientes.join(" ").toLowerCase().includes(ing) &&
      r.via_consumo.toLowerCase().includes(via)
    );
    renderRemedios(filtrado);
  }

  // Cargar los datos del archivo JSON
  $.getJSON("data/remedios.json", function(data) {
    remedios = data;
    renderRemedios(remedios);

    // Añadir eventos de filtro
    $("input").on("input", aplicarFiltros);
  });
});
