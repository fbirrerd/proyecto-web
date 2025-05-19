let filaEnEdicion = false;

$(document).ready(function () {
  //aca se bloquea la pestaña de direcciones
  $("#tab2").addClass("disabled");

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
    // enableTab(2);
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
  const urls = [`usuario/${userid}`,`empresa/list/all`,`empresausuario/usuario/${userid}`];
  fetchMultiple(
    urls,
    function (responses) {
      // [usuarios,direccion,empresas] = responses.map((r) => (r.respuesta ? r.data : []));
      [usuarios, empresas, empresaUsuario] = responses.map((r) => (r.respuesta ? r.data : []));

      if (usuarios) {
        $("#id").val(userid);
        $("#username").val(usuarios.username);
        $("#nombres").val(usuarios.nombres);
        $("#apellidos").val(usuarios.apellidos);
        $("#email").val(usuarios.email);
        $("#duracion").val(usuarios.duracion);
      }

      if(empresas){
        const $contenedor = $("#listaEmpresas");
        $contenedor.empty(); // Limpiar contenido anterior

        empresas.forEach((empresa) => {
          let checked= "";
          if(empresaUsuario.some(eu => eu.id_empresa === empresa.id)){
            checked= "checked";

          }
          
          const checkboxHtml = `
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="empresa_${empresa.id}" value="${empresa.id}" ${checked}>
            <label class="form-check-label" for="empresa_${empresa.id}">${empresa.nombre}</label>
          </div>`;
          $contenedor.append(checkboxHtml);
        });
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

  function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  function validarFormulario() {
    let valido = true;

    // Limpia errores previos
    $(".form-control").removeClass("is-invalid");

    const username = $("#username").val().trim();
    const nombres = $("#nombres").val().trim();
    const apellidos = $("#apellidos").val().trim();
    const email = $("#email").val().trim();
    const duracion = $("#duracion").val().trim();

    if (username === "") {
      $("#username").addClass("is-invalid");
      valido = false;
    }

    if (nombres === "") {
      $("#nombres").addClass("is-invalid");
      valido = false;
    }

    if (apellidos === "") {
      $("#apellidos").addClass("is-invalid");
      valido = false;
    }

    if (duracion === "") {
      $("#duracion").addClass("is-invalid");
      valido = false;
    }

    if (email === "" || !validarEmail(email)) {
      $("#email").addClass("is-invalid");
      valido = false;
    }

    return valido;
  }

  // Puedes llamar esto al hacer clic en un botón guardar
  $("#btnGuardar").click(function (e) {
    e.preventDefault();

    if (validarFormulario()) {
      // Aquí puedes continuar con el submit o enviar por AJAX
      console.log("Formulario válido, se puede enviar");
      let params = {
        username: $("#username").val().trim(),
        nombres: $("#nombres").val().trim(),
        apellidos: $("#apellidos").val().trim(),
        email: $("#email").val().trim(),
        duracion: $("#duracion").val()
      }

      console.log(params);

      callApi("POST", "usuario", params)
        .done(function (response) {
          if (response.respuesta) {
            let id = response.data.id;
            let empresasSeleccionadas = [];

            $('#listaEmpresas input[type="checkbox"]').each(function () {
              empresasSeleccionadas.push({
                id: $(this).val(),
                checked: $(this).is(':checked')
              });
            });

            let params = {
              id: id,
              empresas: empresasSeleccionadas
            }


            callApi("POST", "empresausuario/relacion-empresas", params)
              .done(function (response) {
                if (response.respuesta) {
                  fetchUsuarios();
                  showInfo("Usuario correctamente guardado");    
                  $("#modalUsuario").modal("hide");
                } else {
                  console.log(response.error);
                  showWarning(`Error al guardar la relacion empresas-usuarios. (${response.data.error})`);
                }
              })
              .fail(function () {
                showDanger("No se puede conectar con el servidor");
              });
          } else {
            console.log(response.error);
            showWarning(`Error al guardar el Usuario. (${response.data.error})`);
          }
        })
        .fail(function () {
          showDanger("No se puede conectar con el servidor");
        });



    } else {
      console.warn("Formulario inválido");
    }
  });