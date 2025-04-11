let filaEnEdicion = false;
let roles = [];
let funcionalidades = [];
let rolSeleccionadoId = null;
let currentData = [];

$(document).ready(function() {
    fetchRoles();
    $('#editForm').on('submit', guardarCambios);
});

function fetchRoles() {
    let params;
    callApi('GET', 'rol', params)
    .done(function(response) {
        if (response.respuesta) {
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
    currentData.forEach(rol => {
        const $row = $("<tr>");
        $row.append(
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${rol.id}" value="${rol.nombre}">`),
            $("<td>").append(`
                <select class="form-select form-select-sm" id="estado-${rol.id}">
                    <option value="true" ${rol.estado ? "selected" : ""}>Activo</option>
                    <option value="false" ${!rol.estado ? "selected" : ""}>Inactivo</option>
                </select>
            `),
            $("<td>").append(`
                <button class="btn btn-success btn-sm guardar-btn" data-id="${rol.id}">
                    <i class="fas fa-save"></i> Guardar
                </button>
                <button class="btn btn-warning btn-sm editar-btn" data-id="${rol.id}">
                    <i class="fas fa-edit"></i> Editar
                </button>
            `)
        );
        $tbody.append($row);
    });
}

function mostrarFilaNueva() {
    if (filaEnEdicion) return;
    filaEnEdicion = true;

    const $tbody = $('#tableBody');
    const $fila = $(`
      <tr id="filaNueva">
        <td><input type="text" class="form-control" id="nuevoRolNombre" placeholder="Nombre del rol"></td>
        <td>
          <select class="form-select" id="nuevoRolEstado">
            <option value="true">Activo</option>
            <option value="false">Inactivo</option>
          </select>
        </td>
        <td>
          <button class="btn btn-success btn-sm me-2" onclick="guardarNuevoRol()"><i class="fa fa-check"></i> Guardar</button>
          <button class="btn btn-secondary btn-sm" onclick="cancelarNuevoRol()"><i class="fa fa-times"></i> Cancelar</button>
        </td>
      </tr>
    `);
    $tbody.prepend($fila);
}

async function insertarRol() {
    const nombre = $('#nuevoNombre').val().trim();
    if (!nombre) return alert('Ingresa un nombre');
    await axios.post('/roles', { nombre });
    $('#nuevoNombre').val('');
    cargarRoles();
}

async function actualizarRol(id, nuevoNombre) {
    await axios.put(`/roles/${id}`, { nombre: nuevoNombre });
    cargarRoles();
}


$(document).on("click", ".editar-btn", function () {
    const id = $(this).data("id");
    const rol = currentData.find(r => m.id === id);

    if (!menu) return;
    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();


    rolSeleccionadoId = rolId;
    $('#overlay').show();
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
