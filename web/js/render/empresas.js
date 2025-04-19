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

const tipoOptions = ["link", "padre", "blank","popup"];

function llenarTabla() {
    const $tbody = $("#tableBody");
    $tbody.empty();
    currentData.forEach(item => {
        const $row = $("<tr>");
        
        // Div que simula el select para los iconos
        let icon = item.icono || 'fa-solid fa-house fa-fw';
        let iconObj = iconosFontAwesome.find(i => i.icon === icon) || iconosFontAwesome[0];
        
        let $iconSelectDiv = $(`
          <div class="dropdown">
            <button class="btn dropdown-toggle btn-sm" type="button" id="dropdown-${item.id}" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="${iconObj.icon} me-2"></i> <span class="icon-name">${iconObj.name}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-sm" aria-labelledby="dropdown-${item.id}">
              ${iconosFontAwesome.map(iconObj => `
                <li>
                  <a class="dropdown-item icon-item" href="#"
                    data-icon="${iconObj.icon}"
                    data-name="${iconObj.name}"
                    data-id="${item.id}">
                    <i class="${iconObj.icon} me-2"></i> ${iconObj.name}
                  </a>
                </li>
              `).join('')}
            </ul>
          </div>
          <input type="hidden" id="icono-${item.id}" value="${iconObj.icon}">
        `);
        

        // Agregar el resto de campos de la tabla
        $row.append(
            $("<td>").append($iconSelectDiv),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="nombre-${item.id}" value="${menu.nombre}">`),
            $("<td>").append(`<input type="text" class="form-control form-control-sm small-input" id="ruta-${item.id}" value="${menu.ruta ?? ''}">`),
            $("<td>").append(`<select class="form-select form-select-sm small-input" id="tipo-${item.id}">
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
            // $("<td>").append(`<input type="number" class="form-control form-control-sm" style="width:50px" id="orden-${item.id}" value="${menu.orden}">`),
            $("<td>").append(`
                <button class="btn btn-sm small-btn estado-toggle ${menu.estado ? 'btn-success' : 'btn-secondary'}" data-id="${item.id}">
                    ${menu.estado ? 'Activo' : 'Inactivo'}
                </button>                
                <button class="btn btn-success btn-sm guardar-btn small-btn" data-id="${item.id}"><i class="fas fa-save"></i> </button>
                <button class="btn btn-warning btn-sm editar-btn small-btn" data-id="${item.id}"> <i class="fas fa-edit"></i> 
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
$(document).on('click', '.icon-item', function (e) {
    e.preventDefault();
  
    const newIcon = $(this).data('icon');
    const newName = $(this).data('name');
    const itemId = $(this).data('id');
  
    // Actualizar el ícono y el nombre del botón
    const $btn = $(`#dropdown-${itemId}`);
    $btn.find('i').attr('class', `${newIcon} me-2`);
    $btn.find('.icon-name').text(newName);
  
    // Actualizar input hidden
    $(`#icono-${itemId}`).val(newIcon);
  });

// ✏️ ABRIR MODAL para edición completa
$(document).on("click", ".editar-btn", function () {
    const id = $(this).data("id");
    const menu = currentData.find(r => r.id === id);

    if (!menu) return;

    // Cargar datos en el modal
    $("#editForm [name='id']").val(item.id);
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
