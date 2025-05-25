let currentData = [], empresas = [], usuarios = [], roles = [];
let editModal;

$(function () {
  editModal = new bootstrap.Modal($('#editModal')[0]);
  // $("#editForm").on("submit", guardarCambios);

  const urls = ['empresausuario/list', 'empresa/list/all', 'rol/list/all', 'usuario/list/all'];

  fetchMultiple(urls,
    function (responses) {
      [currentData, empresas, roles, usuarios] = responses.map(r => r.respuesta ? r.data : []);
      cargarTabla();
    },
    function (err) {
      console.error("Fallo global:", err);
    }
  );
});

function cargarTabla() {
  const $tbody = $("#tableBody").empty();

  if (!Array.isArray(currentData)) {
    console.warn("No hay datos válidos para cargar en la tabla.");
    return;
  }

  currentData.forEach(item => {
    const estadoClass = item.estado ? 'btn-success' : 'btn-secondary';
    const estadoTexto = item.estado ? 'Activo' : 'Inactivo';    
    console.log(item);
    const row = `
      <tr>
        <td>${item.empresa_nombre || "Sin nombre"}</td>
        <td>${item.usuario_nombre || "Sin nombre"}</td>
        <td class="acciones-td  text-end">
          <button class="btn btn-sm ${item.estado ? 'btn-success' : 'btn-danger'} btn-estado" 
            data-id-empresa="${item.usuario_id}" data-id-usuario="${item.usuario_id}" title="${item.estado ? 'Desactivar' : 'Activar'}">
            <i class="fas ${item.estado ? 'fa-toggle-on' : 'fa-toggle-off'}"></i>
          </button> 
     
          <button class="btn btn-sm btn-primary" onclick="editarEmpresaUsuario(${item.id_empresa}, ${item.id_usuario})">Editar</button>
        </td>
      </tr>`;
    $tbody.append(row);
  });
}

$("#tableBody").on("click", ".btn-estado", function () {
  const id = $(this).data("id");
  const row = $(this).closest("tr");
  const estadoActual = $(this).hasClass("btn-success");

  const isActivo = this.classList.contains('btn-success');
          
  // Alternar clases
  this.classList.toggle('btn-success', !isActivo);
  this.classList.toggle('btn-danger', isActivo);

  // Cambiar título
  this.title = isActivo ? 'Activar' : 'Desactivar';

  const params = {
    id_empresa: $(this).data("id-empresa"),
    id_usuario: $(this).data("id-usuario"),
    estado: isActivo      
  };

  callApi('PUT', 'empresausuario', params)
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

function agregarFilaInline() {
  const empresaSelect = [`<option value="">Seleccione una empresa</option>`]
    .concat(empresas.map(e => `<option value="${e.id}">${e.nombre}</option>`))
    .join("");

  const usuarioSelect = [`<option value="">Seleccione un usuario</option>`]
    .concat(usuarios.map(u => `<option value="${u.id}">${u.nombreCompleto}</option>`))
    .join("");

  const nuevaFila = `
    <tr id="fila-inline">
      <td>
        <select class="form-select form-select-sm" id="inline-empresa">${empresaSelect}</select>
      </td>
      <td>
        <select class="form-select form-select-sm" id="inline-usuario">${usuarioSelect}</select>
      </td>
      <td class="acciones-td  text-end">
        <button class="btn btn-success btn-sm" onclick="guardarFilaInline()">Guardar</button>
        <button class="btn btn-secondary btn-sm" onclick="$('#fila-inline').remove()">Cancelar</button>
      </td>
    </tr>`;

  $('#fila-inline').remove();
  $('#tableBody').prepend(nuevaFila);
}

function guardarFilaInline() {
  const id_empresa = $('#inline-empresa').val();
  const id_usuario = $('#inline-usuario').val();

  if (!id_empresa || !id_usuario) {
    alert("Debe seleccionar una empresa y un usuario.");
    return;
  }

  const payload = {
    id_empresa,
    id_usuario,
    true:any,
    roles: []
  };

  $.ajax({
    url: "/api/empresa-usuario",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(payload),
    success: function () {
      alert("Registro guardado correctamente");
      $('#fila-inline').remove();
      fetchMultiple(['empresausuario/list'], function ([res]) {
        if (res.respuesta) {
          currentData = res.data;
          cargarTabla();
        }
      });
    },
    error: function () {
      alert("Error al guardar el registro");
    }
  });
}

function editarEmpresaUsuario(idEmpresa, idUsuario) {
  alert("Función de edición en desarrollo");
}

function cancelarNuevaFila() {
  $("#fila-nueva").remove();
}

function guardarNuevoRegistro() {
  const id_empresa = parseInt($("#nueva-empresa").val());
  const id_usuario = parseInt($("#nueva-usuario").val());
  const estado = $("#nuevo-estado").val() === "true";
  const rolesSeleccionados = $("input[type='checkbox']:checked").map(function () {
    return parseInt($(this).val());
  }).get();

  const payload = { id_empresa, id_usuario, estado, roles: rolesSeleccionados };

  $.ajax({
    url: "/api/empresa-usuario",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(payload),
    success: function () {
      alert("Registro guardado correctamente");
      cancelarNuevaFila();
      // Aquí puedes recargar los datos reales desde la API si lo deseas
      fetchMultiple(['empresausuario/list'], function ([res]) {
        if (res.respuesta) {
          currentData = res.data;
          cargarTabla();
        }
      });
    },
    error: function () {
      alert("Error al guardar");
    }
  });
}


function editarEmpresaUsuario(idEmpresa, idUsuario) {
  const data = currentData.find(x => x.id_empresa === idEmpresa && x.id_usuario === idUsuario);
  if (!data) return alert("No se encontró el registro");

  $("#editEmpresaId").val(idEmpresa);
  $("#editUsuarioId").val(idUsuario);
  $("#editEmpresaNombre").val(data.empresa_nombre);
  $("#editUsuarioNombre").val(data.usuario_nombre);

  const rolesAsignados = data.roles.map(r => r.id);
  const contenedor = $("#checkboxRoles");
  contenedor.empty();

  listaRolesDisponibles.forEach(rol => {
      const checked = rolesAsignados.includes(rol.id) ? "checked" : "";
      contenedor.append(`
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value="${rol.id}" id="rol_${rol.id}" ${checked}>
              <label class="form-check-label" for="rol_${rol.id}">${rol.nombre}</label>
          </div>
      `);
  });

  const modal = new bootstrap.Modal(document.getElementById("modalEditarRoles"));
  modal.show();
}

// Guardar roles seleccionados
$("#editForm").on("submit", function (e) {
  e.preventDefault();

  const idEmpresa = $("#editEmpresaId").val();
  const idUsuario = $("#editUsuarioId").val();
  const rolesSeleccionados = $("#checkboxRoles input:checked").map(function () {
      return parseInt(this.value);
  }).get();

  const payload = {
      id_empresa: parseInt(idEmpresa),
      id_usuario: parseInt(idUsuario),
      roles: rolesSeleccionados
  };

  $.ajax({
      url: "/empresa-usuario-rol/update",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function () {
          alert("Roles actualizados correctamente");
          $('#modalEditarRoles').modal('hide');
          // Aquí puedes recargar los datos o actualizar la tabla
      },
      error: function (err) {
          console.error(err);
          alert("Error al actualizar los roles");
      }
  });
});