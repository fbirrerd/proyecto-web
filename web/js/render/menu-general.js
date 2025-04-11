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
    // Informes y Documentos
    "fa-file", "fa-file-alt", "fa-file-pdf", "fa-file-excel", "fa-file-word", 
    "fa-file-powerpoint", "fa-file-archive", "fa-file-contract", "fa-book", 
    "fa-book-open", "fa-clipboard", "fa-clipboard-check", "fa-paste",
  
    // Gráficos y Datos
    "fa-chart-bar", "fa-chart-line", "fa-chart-pie", "fa-database",
  
    // Gestión / Configuración
    "fa-cog", "fa-tools", "fa-wrench", "fa-folder", "fa-folder-open",
    "fa-save", "fa-edit", "fa-sync", "fa-redo", "fa-undo",
  
    // Personas / Usuarios
    "fa-user", "fa-user-circle", "fa-user-edit", "fa-user-plus", 
    "fa-users", "fa-user-friends",
  
    // Tablas / Listas / Estructuras
    "fa-table", "fa-layer-group", "fa-sitemap", "fa-project-diagram",
  
    // Conversaciones / Comunicación
    "fa-comments", "fa-comment", "fa-envelope", "fa-envelope-open",
    "fa-paper-plane", "fa-paperclip", "fa-phone", "fa-mobile-alt",
  
    // Navegación general
    "fa-home", "fa-dashboard", "fa-search", "fa-sign-in-alt", "fa-sign-out-alt",
    "fa-arrow-up", "fa-arrow-down", "fa-arrow-left", "fa-arrow-right"
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
                <select class="form-select form-select-sm small-input" id="padre-${menu.id}">>
                    <option value="">-- Sin padre --</option>
                    ${currentData.filter(m => m.tipo === "padre") // solo padres
                        .map(padre => `
                            <option value="${padre.id}" ${padre.id === menu.id_padre ? "selected" : ""}>
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
        ruta: $(`#ruta-${id}`).val(),
        tipo: $(`#tipo-${id}`).val(),
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
    const menu = currentData.find(r => r.id === id);

    if (!menu) return;

    const $iconoSelect = $("#icono-select");
    $iconoSelect.empty(); // limpiar opciones previas
    icons.forEach(icon => {
        const selected = icon === menu.icono ? 'selected' : '';
        $iconoSelect.append(`
            <option value="${icon}">
                ${icon}
            </option>
        `);
    });

    // 🔽 Llenar select de menús padre
    const $menuPadreSelect = $("#padre-select");
    $menuPadreSelect.empty();
    $menuPadreSelect.append(`<option value="">(Sin padre)</option>`); // opción vacía

    currentData.forEach(m => {
        // Evitar que un menú sea su propio padre
        if (m.id !== id) {
            const selected = m.id === menu.id_padre ? "selected" : "";
            $menuPadreSelect.append(
                `<option value="${m.id}" ${selected}>${m.nombre}</option>`
            );
        }
    });

    // Cargar datos en el modal
    // $("#editForm [name='id']").val(menu.id);
    // $("#editForm [name='nombre']").val(menu.nombre);
    // $("#editForm [name='ruta']").val(menu.ruta);
    // $("#editForm [name='id_padre']").val(menu.id_padre);
    // $("#editForm [name='tipo']").val(menu.tipo);
    // $("#editForm [name='orden']").val(menu.orden);
    // $("#editForm [name='estado']").val(menu.estado.toString());


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
