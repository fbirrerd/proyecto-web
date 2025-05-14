$(document).ready(function () {
    let medicamentos = [];

    function cargarMedicamentos() {
        fetch('medicamentos.json')
            .then(response => {
                if (!response.ok) throw new Error('Error al obtener el archivo JSON');
                return response.json();
            })
            .then(data => {
                medicamentos = data;
                llenarFiltros(data);
                mostrarResultados(data);
            })
            .catch(error => {
                alert("No se pudo cargar el archivo de medicamentos: " + error.message);
            });
    }

    function llenarFiltros(data) {
        const vias = [...new Set(data.map(m => m.viaAdministracion))];
        const labs = [...new Set(data.map(m => m.laboratorio))];
        const disp = [...new Set(data.map(m => m.dispensacion))];

        vias.forEach(v => $('#filtroVia').append(`<option value="${v}">${v}</option>`));
        labs.forEach(l => $('#filtroLaboratorio').append(`<option value="${l}">${l}</option>`));
        disp.forEach(d => $('#filtroDispensacion').append(`<option value="${d}">${d}</option>`));
    }

    function mostrarResultados(resultados) {
        const cont = $('#searchResults');
        cont.empty();
        if (resultados.length === 0) {
            cont.html('<div class="alert alert-warning">No se encontraron medicamentos.</div>');
            return;
        }
        resultados.forEach(m => {
            cont.append(`
                <div class="col-md-4">
                    <div class="card mb-3 h-100">
                        <img src="img/placeholder.png" class="card-img-top" alt="img">
                        <div class="card-body">
                            <h5 class="card-title">${m.nombreComercial}</h5>
                            <p class="card-text"><strong>Principio activo:</strong> ${m.principioActivo}</p>
                            <p class="card-text"><strong>Vía:</strong> ${m.viaAdministracion}</p>
                            <a href="detalle.html?id=${encodeURIComponent(m.nombreComercial)}" class="btn btn-primary">Ver detalle</a>
                        </div>
                    </div>
                </div>
            `);
        });
    }

    function filtrar() {
        const searchTerm = $('#searchInput').val().toLowerCase();
        const via = $('#filtroVia').val();
        const lab = $('#filtroLaboratorio').val();
        const disp = $('#filtroDispensacion').val();

        const res = medicamentos.filter(m =>
            (m.nombreComercial.toLowerCase().includes(searchTerm) || m.principioActivo.toLowerCase().includes(searchTerm)) &&
            (via === '' || m.viaAdministracion === via) &&
            (lab === '' || m.laboratorio === lab) &&
            (disp === '' || m.dispensacion === disp)
        );
        mostrarResultados(res);
    }

    $('#searchInput, #filtroVia, #filtroLaboratorio, #filtroDispensacion').on('input change', filtrar);

    $('#btnMostrarFiltros').on('click', function () {
        $('#filtrosAdicionales').slideToggle();
    });

    cargarMedicamentos();
});
