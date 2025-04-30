
$(document).ready(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const id = parseInt(urlParams.get('id'));

  $.getJSON("data/remedios.json", function(remedios) {
    const remedio = remedios.find(r => r.id === id);
    if (!remedio) return;

    const similares = remedios.filter(r =>
      r.id !== remedio.id &&
      r.ingredientes.includes(remedio.ingredientes[0])
    ).slice(0, 4);

    $("#detalle-remedio").html(`
      <div class="col-md-8">
        <h2>${remedio.nombre}</h2>
        <p><strong>Laboratorio:</strong> ${remedio.laboratorio}</p>
        <p><strong>Presentación:</strong> ${remedio.presentacion}</p>
        <p><strong>Ingredientes:</strong> ${remedio.ingredientes.join(", ")}</p>
        <p><strong>Gramaje:</strong> ${remedio.gramaje}</p>
        <p><strong>Uso:</strong> ${remedio.uso}</p>
        <p><strong>Registro Sanitario:</strong> ${remedio.registro_sanitario}</p>
        <p><strong>Vía de Consumo:</strong> ${remedio.via_consumo}</p>
        <p><strong>Precauciones:</strong> ${remedio.precauciones}</p>
        <p><strong>Contraindicaciones:</strong> ${remedio.contraindicaciones}</p>
        <h4 class="text-success">Precio: ${remedio.precio}</h4>
      </div>
      <div class="col-md-4">
        <img src="img/${remedio.foto}" class="img-fluid rounded mb-3" alt="${remedio.nombre}">
        <h5>Similares</h5>
        <ul class="list-group">
          ${similares.map(s => `<li class="list-group-item"><a href="detalle.html?id=${s.id}">${s.nombre}</a></li>`).join("")}
        </ul>
      </div>
    `);
  });
});
