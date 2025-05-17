let filaEnEdicion = false;

$(document).ready(function () {
  fetchUsuarios();
  $("#btnNuevo").click(function () {
    limpiarFormulario();
    disableTab(2);
    disableTab(3);
    $("#username").prop("disabled", false); // Bloquear
    $("#modalUsuario").modal("show");
  });
  $(document).on("click", ".cambiar-clave-btn", function () {
    const userId = $(this).data("id");
    $('#modalCambiarClave input[name="userId"]').val(userId);
    $("#modalCambiarClave").modal("show");
  });
  $("#openPopup").click(function () {
    $("#password").val("")
    $("#passwordPopup").fadeIn();
  });
  // Cerrar el popup
  $("#closePopup").click(function () {
    $("#passwordPopup").fadeOut();
  });
  // También puedes cerrar al presionar fuera del contenido
  $("#passwordPopup").click(function (e) {
    if (e.target.id === "passwordPopup") {
      $("#passwordPopup").fadeOut();
    }
  });
  // Cuando se hace clic en el botón editar
  $("#tableBody").on("click", ".editar-usuario-btn", function () {
    limpiarFormulario();
    enableTab(2);
    enableTab(3);

    const userId = $(this).data("id");
    const usuario = currentData.find((u) => u.id === userId);

    if (!usuario) {
      alert("Usuario no encontrado");
      return;
    }

    // Cargar los datos en el formulario
    $("#usuarioId").val(usuario.id);
    $("#modalUsuario").modal("show");
    $("#username").prop("disabled", true); // Bloquear
    loadDatosUsuario(usuario.id);
  });
  $("#username").on("blur", function () {
    const username = $(this).val().trim();
    if (username !== "") {
      $("#loading-icon").show(); // 👈 Mostrar ícono

      callApi("GET", `usuario/login/${username}`, null)
        .done(function (response) {
          if (response.respuesta) {
            $("#username").prop("disabled", true); // Bloquear
            loadDatosUsuario(response.data.id);
          } else {
          }
        })
        .fail(function () {
          showDanger("No se puede conectar con el servidor");
        })
        .always(function () {
          $("#loading-icon").hide(); // 👈 Ocultar ícono al terminar
        });
    }
  });
  $("#toggleClave").on("click", function () {
    const input = $("#nuevaClave");
    const icon = $("#iconoClave");

    if (input.attr("type") === "password") {
      input.attr("type", "text");
      icon.removeClass("fa-eye").addClass("fa-eye-slash");
    } else {
      input.attr("type", "password");
      icon.removeClass("fa-eye-slash").addClass("fa-eye");
    }
  });
  $("#tableBody").on("click", ".toggle-estado-btn", function () {
  const $btn = $(this);
  const id = $btn.data("id");
  const estadoActual =
    $btn.data("estado") === true || $btn.data("estado") === "true";
  const nuevoEstado = !estadoActual;

  const params = {
    id: id,
    estado: nuevoEstado,
  };

  callApi("PUT", "usuario/cambiar-estado", params)
    .done(function (response) {
      if (response.respuesta) {
        showInfo("Estado actualizado con éxito");

        // Actualiza visualmente el botón
        $btn.data("estado", nuevoEstado); // Actualiza el data-estado
        if (nuevoEstado) {
          $btn
            .removeClass("btn-danger")
            .addClass("btn-success")
            .html('<i class="bi bi-toggle-on"></i> Activo');
        } else {
          $btn
            .removeClass("btn-success")
            .addClass("btn-danger")
            .html('<i class="bi bi-toggle-off"></i> Inactivo');
        }
      } else {
        showWarning("Hubo un error al intentar actualizar");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
});


});

function enableTab(num) {
  const btn = document.getElementById(`tab${num}`);
  btn.disabled = false;
  btn.classList.add("unlocked-tab");
  $(`tab${num}`).addClass("disabled-tab");
}

function disableTab(num) {
  const btn = document.getElementById(`tab${num}`);
  btn.disabled = true;
  btn.classList.remove("active-tab", "unlocked-tab");
  $(`tab${num}`).removeClass("disabled-tab");
}

function fetchUsuarios() {
  let params;
  callApi("GET", "usuario", params)
    .done(function (response) {
      if (response.respuesta) {
        currentData = response.data;
        llenarTabla();
      } else {
        showDanger("Error en la consulta de la tabla");
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
      $("<td class='acciones-td text-end'>").append(`
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

function limpiarFormulario() {
  const form = document.getElementById("formUsuario");
  const elements = form.querySelectorAll("input, select, textarea");

  elements.forEach((el) => {
    if (el.tagName === "INPUT") {
      if (el.type === "checkbox" || el.type === "radio") {
        el.checked = false;
      } else {
        el.value = "";
      }
    } else if (el.tagName === "SELECT") {
      el.selectedIndex = 0;
    } else if (el.tagName === "TEXTAREA") {
      el.value = "";
    }
  });
}

//cargar datos de usuario
function loadDatosUsuario(userid) {
  // const urls = [`usuario/${usuario.id}`,`direccion/${usuario.id}`,`empresas/usuario/${usuario.id}`];
  const urls = [`usuario/${userid}`];
  fetchMultiple(
    urls,
    function (responses) {
      // [usuarios,direccion,empresas] = responses.map((r) => (r.respuesta ? r.data : []));
      [usuarios] = responses.map((r) => (r.respuesta ? r.data : []));

      if (usuarios) {
        $("#id").val(userid);
        $("#username").val(usuarios.username);
        $("#nombres").val(usuarios.nombres);
        $("#apellidos").val(usuarios.apellidos);
        $("#email").val(usuarios.email);
        $("#username").val(usuarios.username);
        $("#username").val(usuarios.username);
        $("#username").val(usuarios.username);
      }
    },
    function (err) {
      console.error("Fallo global:", err);
    }
  );
}

$("#guardarClaveBtn").on("click", function () {
  const userId = $('#modalCambiarClave input[name="userId"]').val();
  const nuevaClave = $("#nuevaClave").val();
  if (!nuevaClave) return alert("Debe ingresar una nueva clave");

  // Actualiza en la base de datos (AJAX o fetch)
  const params = {
    id: userId,
    password: nuevaClave,
  };

  callApi("PUT", "usuario/cambiar-password", params)
    .done(function (response) {
      if (response.respuesta) {
        showInfo("Clave actualizado con exito");
        $("#passwordPopup").fadeOut();
      } else {
        showWarning("Hubo un error al intentar actualizar");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });  
});
