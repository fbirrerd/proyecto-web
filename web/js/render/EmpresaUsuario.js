let empresas = [];
let usuarios = [];
let roles = [];

$(document).ready(function () {
  cargarDatosIniciales();
});

function cargarDatosIniciales() {
  $.when(
    $.get("/api/empresas"),
    $.get("/api/usuarios"),
    $.get("/api/roles")
  ).done(function (resEmp, resUsu, resRol) {
    empresas = resEmp[0];
    usuarios = resUsu[0];
    roles = resRol[0];

    cargarTabla();
  });
}

function cargarTabla() {
  $.get("/api/empresa-usuario/listado", function (data) {
    const tbody = $("#tbody-empresa-usuario");
    tbody.empty();

    data.forEach(item => {
      const rolesHtml = item.roles.map(r => `<span class="badge bg-info me-1">${r.nombre}</span>`).join("");
      const row = `
        <tr>
          <td>${item.empresa_nombre}</td>
          <td>${item.usuario_nombre}</td>
          <td>${item.estado ? "Activo" : "Inactivo"}</td>
          <td>
            <button class="btn btn-sm btn-primary" onclick="editarEmpresaUsuario(${item.id_empresa}, ${item.id_usuario})">Editar</button>
          </td>
        </tr>`;
      tbody.append(row);
    });
  });
}

function agregarFilaNueva() {
  const tbody = $("#tbody-empresa-usuario");

  const empresaSelect = empresas.map(e => `<option value="${e.id}">${e.nombre}</option>`).join("");
  const usuarioSelect = usuarios.map(u => `<option value="${u.id}">${u.nombre}</option>`).join("");
  const rolesCheckboxes = roles.map(r => `
    <div class="form-check form-check-inline">
      <input class="form-check-input" type="checkbox" value="${r.id}" id="rol-${r.id}">
      <label class="form-check-label" for="rol-${r.id}">${r.nombre}</label>
    </div>
  `).join("");

  const fila = `
    <tr id="fila-nueva">
      <td>
        <select class="form-select" id="nueva-empresa">${empresaSelect}</select>
      </td>
      <td>
        <select class="form-select" id="nueva-usuario">${usuarioSelect}</select>
      </td>
      <td>
        <select class="form-select" id="nuevo-estado">
          <option value="true">Activo</option>
          <option value="false">Inactivo</option>
        </select>
      </td>
      <td>${rolesCheckboxes}</td>
      <td>
        <button class="btn btn-sm btn-success" onclick="guardarNuevoRegistro()">Guardar</button>
        <button class="btn btn-sm btn-secondary" onclick="cancelarNuevaFila()">Cancelar</button>
      </td>
    </tr>
  `;

  $("#fila-nueva").remove(); // elimina fila anterior si existe
  tbody.prepend(fila);
}

function cancelarNuevaFila() {
  $("#fila-nueva").remove();
}

function guardarNuevoRegistro() {
  const id_empresa = parseInt($("#nueva-empresa").val());
  const id_usuario = parseInt($("#nueva-usuario").val());
  const estado = $("#nuevo-estado").val() === "true";
  const roles = $("input[type='checkbox']:checked").map(function () {
    return parseInt($(this).val());
  }).get();

  const payload = {
    id_empresa,
    id_usuario,
    estado,
    roles
  };

  $.ajax({
    url: "/api/empresa-usuario",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(payload),
    success: function () {
      alert("Registro guardado correctamente");
      cargarTabla();
      cancelarNuevaFila();
    },
    error: function () {
      alert("Error al guardar");
    }
  });
}

function editarEmpresaUsuario(idEmpresa, idUsuario) {
  // Aquí puedes llamar a tu modal si quieres edición avanzada
  alert("Función de edición avanzada aquí (modal o inline)");
}