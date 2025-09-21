let medicamentosData = [];
let filteredData = [];
let currentPage = 1;
const itemsPerPage = 8;

$(document).ready(function() {
    fetchRemedios();
});

function fetchRemedios() {
    callApi('GET', 'vademecum/1', null)
    .done(function(response) {
        if (response.respuesta) {
            medicamentosData = response.data;
        } else {
            console.log(response.error);
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });
}

function renderTabla(meds, page = 1) {
    const tbody = document.getElementById("medicamentos-list");
    tbody.innerHTML = "";

    if (meds.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">No se encontraron resultados</td></tr>`;
        document.getElementById("pagination").innerHTML = "";
        return;
    }

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = meds.slice(start, end);

    paginatedItems.forEach(med => {
        const row = `
            <tr>
                <td><img src="img/medicamentos/${med.id_medicamento}.jpg" alt="${med.nombre_comercial}" class="img-thumbnail" style="max-width:80px;"></td>
                <td>${med.nombre_comercial}</td>
                <td>${med.nombre_generico}</td>
                <td><span class="badge bg-primary">${med.nombre_categoria}</span></td>
                <td>${med.nombre_laboratorio}</td>
                <td><a href="detalle_remedios.html?id=${med.id_medicamento}" class="btn btn-sm btn-outline-primary">Ver detalle</a></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    renderPagination(meds, page);
}

function renderCards(meds, page = 1) {
    const container = document.getElementById("vistaCards");
    container.innerHTML = "";

    if (meds.length === 0) return;

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = meds.slice(start, end);

    paginatedItems.forEach(med => {
        const card = `
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="card h-100 shadow-sm">
                    <img src="img/medicamentos/${med.id_medicamento}.jpg" class="card-img-top" alt="${med.nombre_comercial}">
                    <div class="card-footer text-center bg-light">
                        <h6 class="mb-1">${med.nombre_comercial}</h6>
                        <a href="detalle_remedios.html?id=${med.id_medicamento}" class="btn btn-sm btn-outline-primary mt-2">Ver detalle</a>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

function renderPagination(meds, page) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const totalPages = Math.ceil(meds.length / itemsPerPage);
    if (totalPages <= 1) return;

    const createPageItem = (p, label = null, disabled = false, active = false) => {
        const li = document.createElement("li");
        li.className = `page-item ${disabled ? 'disabled' : ''} ${active ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${label || p}</a>`;
        if (!disabled) {
            li.addEventListener('click', e => {
                e.preventDefault();
                currentPage = p;
                renderTabla(filteredData, currentPage);
                renderCards(filteredData, currentPage);
            });
        }
        return li;
    };

    // Botón Primero
    pagination.appendChild(createPageItem(1, "Primero", page === 1));

    let startPage = Math.max(2, page - 2);
    let endPage = Math.min(totalPages - 1, page + 2);

    if (page <= 3) endPage = Math.min(5, totalPages - 1);
    if (page >= totalPages - 2) startPage = Math.max(totalPages - 4, 2);

    // Mostrar páginas intermedias
    for (let i = startPage; i <= endPage; i++) {
        pagination.appendChild(createPageItem(i, null, false, i === page));
    }

    // Botón Último
    pagination.appendChild(createPageItem(totalPages, "Último", page === totalPages));
}

document.getElementById("search").addEventListener("input", function () {
    const term = this.value.toLowerCase();

    if (term.length < 2) {
        document.getElementById("medicamentos-list").innerHTML = `<tr><td colspan="6" class="text-center text-muted">Ingrese al menos 2 letras para buscar</td></tr>`;
        document.getElementById("vistaCards").innerHTML = "";
        document.getElementById("pagination").innerHTML = "";
        filteredData = [];
        currentPage = 1;
        return;
    }

    filteredData = medicamentosData.filter(med =>
        med.nombre_comercial.toLowerCase().includes(term) ||
        med.nombre_generico.toLowerCase().includes(term) ||
        med.nombre_laboratorio.toLowerCase().includes(term) ||
        med.nombre_categoria.toLowerCase().includes(term)
    );

    currentPage = 1;
    renderTabla(filteredData, currentPage);
    renderCards(filteredData, currentPage);
});

// Botón Limpiar
document.getElementById("btnLimpiar").addEventListener("click", () => {
    document.getElementById("search").value = "";
    filteredData = [];
    currentPage = 1;
    document.getElementById("medicamentos-list").innerHTML = `<tr><td colspan="6" class="text-center text-muted">Ingrese al menos 2 letras para buscar</td></tr>`;
    document.getElementById("vistaCards").innerHTML = "";
    document.getElementById("pagination").innerHTML = "";
});

// Cambiar vistas
document.getElementById("btnTabla").addEventListener("click", () => {
    document.getElementById("vistaTabla").classList.remove("d-none");
    document.getElementById("vistaCards").classList.add("d-none");
});

document.getElementById("btnCards").addEventListener("click", () => {
    document.getElementById("vistaTabla").classList.add("d-none");
    document.getElementById("vistaCards").classList.remove("d-none");
});
