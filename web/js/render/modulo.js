let filaEnEdicion = false;
let currentData = [];
let moduloSeleccionadoId = null;

$(document).ready(function() {
    fetchModulos();
});

function fetchModulos() {
    let params;
    callApi('GET', 'modulo', params)
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
    $tbody.empty();

    currentData.forEach(item => {
        const $row = $("<tr>");
        $row.append(
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${item.id}" value="${item.nombre}">`),
            $("<td>").append(`<textarea class="form-control form-control-sm" id="descripcion-${item.id}" rows="2">${item.descripcion || ''}</textarea>`),
            $("<td class='acciones-td text-end'>").append(`
                <div class="form-check form-switch d-inline-block me-2">
                    <input 
                        class="form-check-input toggle-estado-switch" 
                        type="checkbox" 
                        role="switch"
                        data-id="${item.id}"
                        ${item.estado ? 'checked' : ''}>
                </div>
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

function mostrarFilaNueva() {
    if (filaEnEdicion) return;
    filaEnEdicion = true;

    const $tbody = $('#tableBody');
    const $fila = $(`
        <tr id="filaNueva">
            <td><input type="text" class="form-control form-control-sm" id="nuevoModuloNombre" placeholder="Nombre del módulo"></td>
            <td><input type="text" class="form-control form-control-sm" id="nuevoModuloDescripcion" placeholder="Descripción del módulo"></td>
            <td class="text-end">
                <button class="btn btn-success btn-sm me-2" onclick="insertarModulo()"><i class="fa fa-check"></i> Guardar</button>
                <button class="btn btn-secondary btn-sm" onclick="cancelarNuevoModulo()"><i class="fa fa-times"></i> Cancelar</button>
            </td>
        </tr>
    `);
    $tbody.prepend($fila);
}

function cancelarNuevoModulo() {
    $('#filaNueva').remove();
    filaEnEdicion = false;
}

function insertarModulo() {
    const nombre = $('#nuevoModuloNombre').val().trim();
    const descripcion = $('#nuevoModuloDescripcion').val().trim();

    if (!nombre) {
        alert('Ingresa un nombre');
        return;
    }

    axios.post('/api/modulo', { nombre, descripcion, estado: true })
        .then(response => {
            if (response.data.respuesta) {
                showSuccess("Módulo guardado correctamente");
                cancelarNuevoModulo();
                fetchModulos();
            } else {
                console.error(response.data.error);
                showWarning(`Error al guardar el módulo: ${response.data.error}`);
            }
        })
        .catch(() => {
            showDanger("No se puede conectar con el servidor");
        });
}

// Toggle estado usando delegación
$('#tableBody').on("change", ".toggle-estado-switch", function () {
    const id = $(this).data("id");
    const nuevoEstado = $(this).is(":checked");

    axios.put(`/api/modulo/${id}/estado`, { estado: nuevoEstado })
        .then(() => {
            showSuccess(`Estado actualizado a ${nuevoEstado ? 'Activo' : 'Inactivo'}`);
        })
        .catch(() => {
            showDanger("Error al actualizar el estado.");
            fetchModulos(); // Revertir cambios visuales si falla
        });
});

// Botón editar
$('#tableBody').on("click", ".editar-btn", function () {
    const id = $(this).data("id");
    moduloSeleccionadoId = id;

    const modulo = currentData.find(m => m.id === id);

    if (!modulo) {
        alert("Módulo no encontrado.");
        return;
    }

    // Llenar modal con datos
    $('#modalModuloNombre').text(modulo.nombre);
    $('#moduloModal').modal('show');

    // Aquí puedes agregar llamadas como:
    cargarInventarioModulo(id);
    cargarEmpresasModulo(id);
    cargarMenusModulo(id);
});

// Guardar permisos del modal
async function guardarPermisos() {
    const seleccionados = $('#funcionalidadesLista input:checked').map(function() {
        return parseInt($(this).val());
    }).get();

    try {
        await axios.post(`/api/modulo/${moduloSeleccionadoId}/permisos`, { funcionalidades: seleccionados });
        cerrarPopup();
        showSuccess("Permisos guardados correctamente");
    } catch (error) {
        showDanger("Error al guardar permisos");
    }
}

function cerrarPopup() {
    $('#overlay').hide();
    $('#popup').hide();
    moduloSeleccionadoId = null;
}
