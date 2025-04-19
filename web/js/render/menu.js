let currentData = [];
let editModal;

document.addEventListener("DOMContentLoaded", () => {
    fetchitems();
    editModal = new bootstrap.Modal(document.getElementById('editModal'));
    document.getElementById("editForm").addEventListener("submit", guardarCambios);
});

function fetchitems() {
    let params;
    callApi('GET', 'menu/generales', params)
    .done(function(response) {
        if (response.respuesta) {
            currentData = response.data;
            llenarTabla();            
        } else {
            // Si hay un error en la respuesta
            console.log(response.error);
            $('#error-message').text(`Error en el login. Verifica tus credenciales. (${response.data.error})`).removeClass('d-none');
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });

}

const tipoOptions = ["link", "padre", "blank","popup"];

function llenarTabla() {
    const $tbody = $("#tableBody");
    $tbody.empty();
    currentData.forEach(item => {
        const $row = $("<tr>");

        // Div que simula el select para los iconos
        let $iconSelectDiv = $(`
            <div class="dropdown">
                <button class="btn dropdown-toggle btn-sm" type="button" id="dropdown-${item.id}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas ${item.icono} me-2"></i> Seleccione
                </button>
                <ul class="dropdown-menu dropdown-menu-sm" style="max-height: 200px; overflow-y: auto; font-size: 0.85rem;" aria-labelledby="dropdown-${item.id}">
                    ${iconosFontAwesome.map(icon => `
                        <li><a class="dropdown-item icon-item" href="#" data-icon="${icon.name}"><i class="fas ${icon.icon} me-2"></i> ${icon.name}</a></li>
                    `).join('')}
                </ul>
                </div>
                <input type="hidden" id="icono-${item.id}" value="${item.icon}">
        `);

        // Agregar el resto de campos de la tabla
        $row.append(
            $("<td>").append($iconSelectDiv),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="nombre-${item.id}" value="${item.nombre}">`),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="ruta-${item.id}" value="${item.url ?? ''}">`),
            // $("<td>").append(`<select class="form-select form-select-sm small-input" id="tipo-${item.id}">
            //     ${tipoOptions.map(tipo => `<option value="${tipo}" ${tipo === item.tipo ? "selected" : ""}>${tipo}</option>`).join('')}
            // </select>`),
            $("<td>").append(`
                <select class="form-select form-select-sm small-input" id="padre-${item.id}">>
                    <option value="">-- Sin padre --</option>
                    ${currentData // solo padres
                        .map(padre => `
                            <option value="${padre.id}" ${padre.id === item.id_padre ? "selected" : ""}>
                                ${padre.nombre}
                            </option>
                        `).join('')}
                </select>
            `),
            // $("<td>").append(`<input type="number" class="form-control form-control-sm" style="width:50px" id="orden-${item.id}" value="${item.orden}">`),
            $("<td>").append(`
                <button class="btn btn-sm small-btn estado-toggle ${item.estado ? 'btn-success' : 'btn-secondary'}" data-id="${item.id}">
                    ${item.estado ? 'Activo' : 'Inactivo'}
                </button>
                <button class="btn btn-secondary btn-sm guardar-btn small-btn" data-id="${item.id}">
                    <i class="fas fa-save"></i>
                </button>
                <button class="btn btn-secondary btn-sm editar-btn small-btn" data-id="${item.id}">
                    <i class="fas fa-edit"></i>
                </button>
            `)
        );

        $tbody.append($row);
    });
}

$(document).on("click", ".estado-toggle", function () {
    const $btn = $(this);
    const id = $btn.data("id");
    const currentEstado = $btn.hasClass("btn-success");

    // Cambiar visual
    $btn
        .toggleClass("btn-success btn-secondary")
        .text(currentEstado ? "Inactivo" : "Activo");

    // Actualizar el hidden input si lo necesitas
    $(`#estado-${id}`).val(!currentEstado);

    // Actualizar directamente si deseas (opcional)
    const params = {
        id: id,
        estado: !currentEstado
    };

    callApi('PUT', 'menu/cambiar-estado', params)
    .done(function(response) {
        if (response.respuesta) {
            showInfo("Estado actualizado con exito");          
        } else {
            showWarning("Hubo un error al intentar actualizar");            
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor");          
    });
});

// 🟢 GUARDAR cambios desde la fila
$(document).on("click", ".guardar-btn", function () {
    const id = $(this).data("id");

    const params = {
        id: id,
        nombre: $(`#nombre-${id}`).val(),
        icono: $(`#icono-${id}`).val(),
        url: $(`#ruta-${id}`).val(),
        id_padre: $(`#padre-${id}`).val() || null // Si está vacío, usa null
    };

    callApi('PUT', 'menu/generales', params)
    .done(function(response) {
        if (response.respuesta) {
            currentData = response.data;
            showInfo("Estado actualizado con exito");
            llenarTabla();            
        } else {
            showWarning("Hubo un error al intentar actualizar");
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor");          
    });
    
});

// Asignar icono al seleccionar una opción
$(document).on("click", ".icon-item", function () {
    const icon = $(this).data("icon");
    const id = $(this).closest(".dropdown").find("button").attr("id").split('-')[1];
    
    // Actualizar el ícono visible en el botón del dropdown
    $(this).closest(".dropdown").find("button").html(`<i class="fas ${icon} me-2"></i> ${icon}`);
    
    // Actualizar el valor del input oculto
    $(`#icono-${id}`).val(icon);
});

// ✏️ ABRIR MODAL para edición completa
$(document).on("click", ".editar-btn", function () {
    const id = $(this).data("id");
    const item = currentData.find(r => r.id === id);

    if (!item) return;

    const $iconoSelect = $("#icono-select");
    $iconoSelect.empty(); // limpiar opciones previas
    iconosFontAwesome.forEach(icon => {
        const selected = icon === item.icono ? 'selected' : '';
        $iconoSelect.append(`
            <option value="${icon}">
                ${icon}
            </option>
        `);
    });

    // 🔽 Llenar select de menús padre
    const $itemPadreSelect = $("#padre-select");
    $itemPadreSelect.empty();i
    $itemPadreSelect.append(`<option value="">(Sin padre)</option>`); // opción vacía

    currentData.forEach(m => {
        // Evitar que un menú sea su propio padre
        if (m.id !== id) {
            const selected = m.id === item.id_padre ? "selected" : "";
            $itemPadreSelect.append(
                `<option value="${m.id}" ${selected}>${m.nombre}</option>`
            );
        }
    });

    // Cargar datos en el modal
    // $("#editForm [name='id']").val(item.id);
    // $("#editForm [name='nombre']").val(item.nombre);
    // $("#editForm [name='ruta']").val(item.ruta);
    // $("#editForm [name='id_padre']").val(item.id_padre);
    // $("#editForm [name='tipo']").val(item.tipo);
    // $("#editForm [name='orden']").val(item.orden);
    // $("#editForm [name='estado']").val(item.estado.toString());


    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();
});



function editar(id) {
    const item = currentData.find(m => m.id === id);
    if (!item) return;

    const form = document.getElementById("editForm");
    for (let key in item) {
        if (form[key] !== undefined) {
            form[key].value = item[key];
        }
    }
    editModal.show();
}

function guardarCambios(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    data.id = parseInt(data.id);
    data.orden = parseInt(data.orden);
    data.estado = data.estado === "true";
    data.es_publico = false;
    data.icono = "";
    data.fecha_creacion = new Date().toISOString();
    data.fecha_modificacion = new Date().toISOString();

    fetch("/item", {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => res.json())
      .then(() => {
        editModal.hide();
        fetchitems();
      });
}
