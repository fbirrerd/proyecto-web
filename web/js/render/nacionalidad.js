let filaEnEdicion = false;
let nacionalidades = [];
let funcionalidades = [];
let nacionalidadSeleccionadaId = null;
let currentData = [];

$(document).ready(function() {
    fetchNacionalidades();
});

function fetchNacionalidades() {
    let params;
    callApi('GET', 'nacionalidad', params)
    .done(function(response) {
        if (response.respuesta) {
            currentData = response.data;
            llenarTabla();            
        } else {
            console.log(response.error);
            $('#error-message').text(`Error al cargar nacionalidades. (${response.data.error})`).removeClass('d-none');
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
            $("<td>").append(`<input type="text" class="form-control form-control-sm" id="nombre-${item.id}" value="${item.nombre}">`),
            $("<td class='acciones text-end'>").append(`
                <button 
                    class="btn btn-sm ${item.estado ? 'btn-success' : 'btn-danger'} btn-estado" 
                    data-id="${item.id}"
                    title="${item.estado ? 'Desactivar' : 'Activar'}"
                >
                    <i class="fas ${item.estado ? 'fa-toggle-on' : 'fa-toggle-off'}"></i>
                </button>         
                <button class="btn btn-success btn-sm guardar-btn" data-id="${item.id}">
                    <i class="fas fa-save"></i>
                </button>
            `)
        );
        $tbody.append($row);
    });
}

$("#tableBody").on("click", ".guardar-btn", function () {
    const row = $(this).closest("tr");
    const id = row.data("id");
    const nombre = row.find(".nombre").val();

    const params = {
        nombre: nombre
    }

    callApi('PUT', `nacionalidad/${id}`, params)
        .done(function(response) {
            if (response.respuesta) {
                showInfo("Guardado correctamente");
            } else {
                showWarning("Error al guardar");
            }
        })
        .fail(function() {
            showDanger("No se puede conectar con el servidor"); 
        });
});

$("#tableBody").on("click", ".btn-estado", function () {
    const id = $(this).data("id");
    const row = $(this).closest("tr");
    const nombre = row.find(".nombre").val();
    const estadoActual = $(this).hasClass("btn-success");

    const params = {
        estado: !estadoActual
    }

    callApi('PUT', `nacionalidad/${id}`, params)
        .done(function(response) {
            if (response.respuesta) {
                fetchNacionalidades();
            } else {
                showWarning("Error al actualizar estado de nacionalidad");
            }
        })
        .fail(function() {
            showDanger("No se puede conectar con el servidor"); 
        });
});

function mostrarFilaNueva() {
    if (filaEnEdicion) return;
    filaEnEdicion = true;

    const $tbody = $('#tableBody');
    const $fila = $(`
        <tr id="filaNueva">
            <td><input type="text" class="form-control" id="nuevaNacionalidadNombre" placeholder="Nombre de la nacionalidad"></td>
            <td class="acciones text-end">
                <button class="btn btn-success btn-sm me-2" onclick="insertarNacionalidad()"><i class="fa fa-check"></i> Guardar</button>
                <button class="btn btn-secondary btn-sm" onclick="cancelarNuevaNacionalidad()"><i class="fa fa-times"></i> Cancelar</button>
            </td>
        </tr>
    `);
    $tbody.prepend($fila);
}

async function insertarNacionalidad() {
    const nombre = $('#nuevaNacionalidadNombre').val();
    if (!nombre) return alert('Ingresa un nombre');
    let params = {
        "nombre": nombre,
        "estado": true
    }
    callApi('POST', 'nacionalidad', params)
        .done(function(response) {
            if (response.respuesta) {
                fetchNacionalidades();
            } else {
                console.log(response.error);
                showWarning(`Error al guardar la nacionalidad. (${response.data.error})`);
            }
        })
        .fail(function() {
            showDanger("No se puede conectar con el servidor"); 
        });
    $('#nuevaNacionalidadNombre').val('');
}

async function actualizarNacionalidad(id, nuevoNombre) {
    await axios.put(`/nacionalidades/${id}`, { nombre: nuevoNombre });
    fetchNacionalidades();
}

$("#tableBody").on("click", ".toggle-estado-btn", function () {
    const $btn = $(this);
    const id = $btn.data("id");
    const estadoActual = $btn.data("estado") === true || $btn.data("estado") === "true";
    const nuevoEstado = !estadoActual;

    $.ajax({
        url: `/api/actualizar-estado/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({ estado: nuevoEstado }),
        success: function () {
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
    const nacionalidad = currentData.find(n => n.id === id);

    if (!nacionalidad) return;

    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();

    nacionalidadSeleccionadaId = id;
    $('#popup').show();

    const menus = fetchMenus();

    const contenedor = $('#funcionalidadesLista');
    contenedor.html(menus.map(m => `
        <label><input type="checkbox" value="${m.id}"> ${m.nombre}</label><br>
    `).join(''));
});



function cancelarNuevaNacionalidad() {
    $('#filaNueva').remove();
    filaEnEdicion = false;
}
