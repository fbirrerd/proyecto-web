let filaEnEdicion = false;
let usuarios = [];

$(document).ready(function () {
  fetchUsuarios();
  $("#btnNuevo").click(function () {
    $("#modalUsuario").modal("show");
  });
});

function fetchUsuarios() {
  let params;
  callApi("GET", "usuario", params)
    .done(function (response) {
      if (response.respuesta) {
        console.log(response.data);
        currentData = response.data;
        llenarTabla();
      } else {
        console.log(response.error);
        $("#error-message")
          .text(
            `Error en el login. Verifica tus credenciales. (${response.data.error})`
          )
          .removeClass("d-none");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

function llenarTabla() {
  const $tbody = $("#tableBody");
  $tbody.empty(); // Limpiar la tabla antes de llenar

  currentData.forEach((item) => {
    const $row = $("<tr>");

    $row.append(
      $("<td>").text(item.username),
      $("<td>").text(item.nombres),
      $("<td>").text(item.email),

      // Columna de acciones
      $("<td class='acciones text-end'>").append(`
                <button 
                    class="btn btn-sm toggle-estado-btn ${
                      item.estado ? "btn-success" : "btn-secondary"
                    }" 
                    data-id="${item.id}" 
                    data-estado="${item.estado}">
                    <i class="fas ${
                      item.estado ? "fa-toggle-on" : "fa-toggle-off"
                    }"></i>
                </button>

                <button class="btn btn-primary btn-sm cambiar-clave-btn" data-id="${
                  item.id
                }">
                    <i class="fas fa-key"></i>
                </button>

                <button class="btn btn-warning btn-sm editar-usuario-btn" data-id="${
                  item.id
                }">
                    <i class="fas fa-edit"></i>
                </button>
            `)
    );

    $tbody.append($row);
  });
}

async function insertarUsuario() {
  const nombre = $("#nuevoRolNombre").val();
  if (!nombre) return alert("Ingresa un nombre");
  let params = {
    nombre: nombre,
    estado: true,
  };
  callApi("POST", "rol", params)
    .done(function (response) {
      if (response.respuesta) {
        return response.data;
      } else {
        console.log(response.error);
        showWarning(`Error al guardar el Rol. (${response.data.error})`);
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
  $("#nuevoRolNombre").val("");
  fetchRoles();
}

$("#tableBody").on("click", ".toggle-estado-btn", function () {
  const $btn = $(this);
  const id = $btn.data("id");
  const estadoActual =
    $btn.data("estado") === true || $btn.data("estado") === "true";
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
    },
  });
});


$("#guardarClaveBtn").on("click", function () {
  const userId = $('#modalCambiarClave input[name="userId"]').val();
  const nuevaClave = $("#nuevaClave").val();
  if (!nuevaClave) return alert("Debe ingresar una nueva clave");

  callApi("PUT", `usuario/${userId}/clave`, { password: nuevaClave })
    .done(() => {
      $("#modalCambiarClave").modal("hide");
      showSuccess("Contraseña actualizada");
    })
    .fail(() => showDanger("Error al actualizar la contraseña"));
});

// Mostrar el popup al hacer clic en el botón

// Acción cuando se presiona "Aceptar"
$("#submitPassword").click(function () {
  const password = $("#passwordInput").val();
  alert("Contraseña ingresada: " + password);
  $("#passwordPopup").fadeOut(); // Cierra después de enviar
});



