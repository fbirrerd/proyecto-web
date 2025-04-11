let currentData = [];
let editModal;

document.addEventListener("DOMContentLoaded", () => {
    fetchMenus();
    editModal = new bootstrap.Modal(document.getElementById('editModal'));
    document.getElementById("editForm").addEventListener("submit", guardarCambios);
});

function fetchMenus() {
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

const icons = [
    "fa-home","fa-dashboard", "fa-user", "fa-lock", "fa-cog", "fa-envelope", "fa-search",
    "fa-check", "fa-times", "fa-plus", "fa-minus", "fa-edit", "fa-trash",
    "fa-download", "fa-upload", "fa-save", "fa-camera", "fa-calendar", "fa-clock",
    "fa-bell", "fa-heart", "fa-star", "fa-user-plus", "fa-user-edit", "fa-user-circle",
    "fa-users", "fa-user-friends", "fa-globe", "fa-map-marker-alt", "fa-compass",
    "fa-chart-bar", "fa-chart-line", "fa-chart-pie", "fa-comments", "fa-comment",
    "fa-envelope-open", "fa-folder", "fa-folder-open", "fa-file", "fa-file-alt",
    "fa-file-pdf", "fa-file-image", "fa-link", "fa-external-link-alt", "fa-phone",
    "fa-mobile-alt", "fa-laptop", "fa-desktop", "fa-tablet-alt", "fa-print",
    "fa-shopping-cart", "fa-cart-plus", "fa-credit-card", "fa-wallet", "fa-gift",
    "fa-barcode", "fa-qrcode", "fa-tag", "fa-tags", "fa-bolt", "fa-lightbulb",
    "fa-info-circle", "fa-question-circle", "fa-exclamation-circle", "fa-exclamation-triangle",
    "fa-shield-alt", "fa-lock-open", "fa-key", "fa-wifi", "fa-signal",
    "fa-cog", "fa-wrench", "fa-tools", "fa-sync", "fa-redo", "fa-undo",
    "fa-arrow-up", "fa-arrow-down", "fa-arrow-left", "fa-arrow-right",
    "fa-long-arrow-alt-up", "fa-long-arrow-alt-down", "fa-long-arrow-alt-left", "fa-long-arrow-alt-right",
    "fa-sign-in-alt", "fa-sign-out-alt", "fa-share", "fa-share-alt", "fa-upload",
    "fa-play", "fa-pause", "fa-stop", "fa-forward", "fa-backward",
    "fa-volume-up", "fa-volume-down", "fa-volume-mute", "fa-microphone", "fa-headphones",
    "fa-image", "fa-images", "fa-video", "fa-music", "fa-film",
    // Íconos adicionales para documentos y programas
    "fa-file-word", "fa-file-excel", "fa-file-powerpoint", "fa-file-archive",
    "fa-file-code", "fa-file-audio", "fa-file-video", "fa-file-contract",
    "fa-book", "fa-book-open", "fa-bookmark", "fa-clipboard", "fa-clipboard-check",
    "fa-paste", "fa-paperclip", "fa-paper-plane", "fa-project-diagram", "fa-sitemap",
    "fa-database", "fa-code-branch", "fa-network-wired", "fa-server",
    "fa-laptop-code", "fa-terminal", "fa-layer-group", "fa-vector-square"
];
icons.sort();

const tipoOptions = ["link", "padre", "blank","popup"];

function llenarTabla() {
    const $tbody = $("#tableBody");
    $tbody.empty();
    currentData.forEach(menu => {
        const $row = $("<tr>");
        
        // Div que simula el select para los iconos
        let $iconSelectDiv = $(`
            <div class="dropdown">
                <button class="btn dropdown-toggle btn-sm" type="button" id="dropdown-${menu.id}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas ${menu.icono} me-2"></i> Seleccione
                </button>
                <ul class="dropdown-menu dropdown-menu-sm" aria-labelledby="dropdown-${menu.id}">
                    ${icons.map(icon => `
                        <li><a class="dropdown-item icon-item" href="#" data-icon="${icon}"><i class="fas ${icon} me-2"></i> ${icon}</a></li>
                    `).join('')}
                </ul>
            </div>
            <input type="hidden" id="icono-${menu.id}" value="${menu.icono}">
        `);

        // Agregar el resto de campos de la tabla
        $row.append(
            $("<td>").append($iconSelectDiv),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="nombre-${menu.id}" value="${menu.nombre}">`),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="ruta-${menu.id}" value="${menu.ruta ?? ''}">`),
            $("<td>").append(`<select class="form-select form-select-sm small-input" id="tipo-${menu.id}">
                ${tipoOptions.map(tipo => `<option value="${tipo}" ${tipo === menu.tipo ? "selected" : ""}>${tipo}</option>`).join('')}
            </select>`),
            $("<td>").append(`
                <select class="form-select form-select-sm small-input" name="padre_id">
                    <option value="">-- Sin padre --</option>
                    ${currentData.filter(m => m.tipo === "padre") // solo padres
                        .map(padre => `
                            <option value="${padre.id}" ${padre.id === menu.padre_id ? "selected" : ""}>
                                ${padre.nombre}
                            </option>
                        `).join('')}
                </select>
            `),
            // $("<td>").append(`<input type="number" class="form-control form-control-sm" style="width:50px" id="orden-${menu.id}" value="${menu.orden}">`),
            $("<td>").append(`
                <button class="btn btn-sm small-btn estado-toggle ${menu.estado ? 'btn-success' : 'btn-secondary'}" data-id="${menu.id}">
                    ${menu.estado ? 'Activo' : 'Inactivo'}
                </button>                
                <button class="btn btn-success btn-sm guardar-btn small-btn" data-id="${menu.id}">
                    <i class="fas fa-save"></i> Guardar
                </button>
                <button class="btn btn-warning btn-sm editar-btn small-btn" data-id="${menu.id}">
                    <i class="fas fa-edit"></i> Editar
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
    .done(() => {
        if (response.respuesta) {
            currentData = response.data;
            mostrarAlerta({
                mensaje: "Actualizado con éxito",
                tipo: "success",
                duracion: 5 // 5 segundos
            });            
            llenarTabla();            
        } else {
            mostrarAlerta({
                mensaje: "Hubo un error al intentar actualizar",
                tipo: "danger",
                duracion: 5 // 5 segundos
            });            
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
        ruta: $(`#ruta-${id}`).val(),
        tipo: $(`#tipo-${id}`).val(),
        orden: parseInt($(`#orden-${id}`).val()),
        estado: $(`#estado-${id}`).val() === "true"
    };
    callApi('PUT', 'menu/generales', params)
    .done(function(response) {
        if (response.respuesta) {
            currentData = response.data;
            mostrarAlerta({
                mensaje: "Actualizado con éxito",
                tipo: "success",
                duracion: 5 // 5 segundos
            });            
            llenarTabla();            
        } else {
            mostrarAlerta({
                mensaje: "Hubo un error al intentar actualizar",
                tipo: "danger",
                duracion: 5 // 5 segundos
            });            
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
    const menu = currentData.find(r => r.id === id);

    if (!menu) return;

    // Cargar datos en el modal
    $("#editForm [name='id']").val(menu.id);
    $("#editForm [name='nombre']").val(menu.nombre);
    $("#editForm [name='ruta']").val(menu.ruta);
    $("#editForm [name='tipo']").val(menu.tipo);
    $("#editForm [name='orden']").val(menu.orden);
    $("#editForm [name='estado']").val(menu.estado.toString());

    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();
});



function editar(id) {
    const menu = currentData.find(m => m.id === id);
    if (!menu) return;

    const form = document.getElementById("editForm");
    for (let key in menu) {
        if (form[key] !== undefined) {
            form[key].value = menu[key];
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

    fetch("/menu", {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => res.json())
      .then(() => {
        editModal.hide();
        fetchMenus();
      });
}
