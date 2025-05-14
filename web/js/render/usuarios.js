let filaEnEdicion = false;
let usuarios = [];
let funcionalidades = 

$(document).ready(function() {
    fetchUsuarios();
    $('#editForm').on('submit', guardarCambios);
});

function fetchUsuarios() {
    let params;
    callApi('GET', 'usuario', params)
    .done(function(response) {
        if (response.respuesta) {
            console.log(response.data)
            currentData = response.data;
            llenarTabla();            
        } else {
            console.log(response.error);
            $('#error-message').text(`Error en el login. Verifica tus credenciales. (${response.data.error})`).removeClass('d-none');
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });
}

function llenarTabla() {
    const $tbody = $("#tableBody");
    $tbody.empty(); // Limpiar la tabla antes de llenar
    currentData.forEach(item => {
        const $row = $("<tr>");
        $row.append(
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${item.id}" value="${item.username}">`),
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${item.id}" value="${item.nombres}">`),
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${item.id}" value="${item.email}">`),
            $("<td class='acciones-td  text-end'>").append(`
                <button 
                    class="btn btn-sm toggle-estado-btn ${item.estado ? 'btn-success' : 'btn-secondary'}" 
                    data-id="${item.id}" 
                    data-estado="${item.estado}">
                    ${item.estado ? 'Activo' : 'Inactivo'}
                </button>                
                <button class="btn btn-success btn-sm guardar-btn" data-id="${item.id}">
                    <i class="fas fa-save"></i>
                </button>
                <button class="btn btn-warning btn-sm editar-btn" data-id="${item.id}">
                    <i class="fas fa-edit"></i>
                </button>
            `)
        );
        $tbody.append($row);
    });
}

async function insertarUsuario() {
    const nombre = $('#nuevoRolNombre').val();
    if (!nombre) return alert('Ingresa un nombre');
    let params = {
        "nombre": nombre,
        "estado": true
      }
    callApi('POST', 'rol', params)
    .done(function(response) {
        if (response.respuesta) {
            return response.data;
        } else {
            console.log(response.error);
            showWarning(`Error al guardar el Rol. (${response.data.error})`);
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });
    $('#nuevoRolNombre').val('');
    fetchRoles();
}

async function actualizarRol(id, nuevoRolNombre) {
    await axios.put(`/roles/${id}`, { nombre: nuevoRolNombre });
    fetchRoles();
}

$tbody.on("click", ".toggle-estado-btn", function () {
    const $btn = $(this);
    const id = $btn.data("id");
    const estadoActual = $btn.data("estado") === true || $btn.data("estado") === "true";
    const nuevoEstado = !estadoActual;

    // Actualiza en la base de datos (AJAX o fetch)
    $.ajax({
        url: `/api/actualizar-estado/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({ estado: nuevoEstado }),
        success: function () {
            // Actualiza el botón visualmente
            $btn
                .data("estado", nuevoEstado)
                .removeClass("btn-success btn-secondary")
                .addClass(nuevoEstado ? "btn-success" : "btn-secondary")
                .text(nuevoEstado ? "Activo" : "Inactivo");
        },
        error: function () {
            alert("Error al actualizar el estado.");
        }
    });
});

$(document).on("click", ".editar-btn", function () {
    const id = $(this).data("id");
    const rol = currentData.find(r => m.id === id);

    if (!menu) return;
    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();


    rolSeleccionadoId = rolId;
    $('#popup').show();
  
    const menus = fetchMenus()

    const contenedor = $('#funcionalidadesLista');
    contenedor.html(menus.map(m => `
        <label><input type="checkbox" value="${m.id}"> ${m.nombre}</label><br>
    `).join(''));
    
    
});

function fetchMenus() {
    let params;
    callApi('GET', 'menu-tree', params)
    .done(function(response) {
        if (response.respuesta) {
            return response.data;
        } else {
            console.log(response.error);
            $('#error-message').text(`Error en el login. Verifica tus credenciales. (${response.data.error})`).removeClass('d-none');
        }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });
}

function cerrarPopup() {
    $('#overlay').hide();
    $('#popup').hide();
    rolSeleccionadoId = null;
}

async function guardarPermisos() {
    const seleccionados = $('#funcionalidadesLista input:checked').map(function() {
        return parseInt($(this).val());
    }).get();
    await axios.post(`/roles/${rolSeleccionadoId}/permisos`, { funcionalidades: seleccionados });
    cerrarPopup();
}

function cancelarNuevoRol() {
    $('#filaNueva').remove();
    filaEnEdicion = false;
}
