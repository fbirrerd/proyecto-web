let currentData = [],
    tipoEmpresas = [],
    modulos = [],
    modulosSeleccionados = [];

$(document).ready(() => {
  cargarConsultas();

  $("#formEmpresa").submit(function (e) {
    e.preventDefault();
    guardarEmpresa();
  });

  // Delegación para los botones de estado, aunque generes dinámicamente
  $(document).on("click", ".btn-estado", function () {
    const btn = $(this);
    const id = btn.data("id");
    const icon = btn.find("i");
    const estadoActual = icon.hasClass("fa-toggle-on");
    const nuevoEstado = !estadoActual;
    cambiarEstado(id, nuevoEstado);
  });
});

function cargarConsultas() {
  const urls = ["empresa", "tipoempresa/list/all", "modulo"];
  fetchMultiple(
    urls,
    function (responses) {
      [currentData, tipoEmpresas, modulos] = responses.map(r => (r.respuesta ? r.data : []));
      cargarEmpresas();
      cargarTiposEmpresa();
      cargarModulos();
    },
    function (err) {
      console.error("Fallo global:", err);
    }
  );
}

function cargarTiposEmpresa() {
  $("#tipoEmpresa").html(
    '<option value="">Seleccione</option>' +
      tipoEmpresas.map(t => `<option value="${t.id}">${t.nombre}</option>`).join("")
  );
}

function cargarEmpresas() {
  const rows = currentData.map(item => `
    <tr>
      <td><input class="form-control form-control-sm" value="${item.nombre}"
        onchange="editarCampo(${item.id}, 'nombre', this.value)"></td>
      <td>
        <select class="form-select form-select-sm"
          onchange="editarCampo(${item.id}, 'id_tipo_empresa', this.value)">
          ${tipoEmpresas.map(t => `
            <option value="${t.id}" ${t.id === item.id_tipo_empresa ? "selected" : ""}>${t.nombre}</option>
          `).join("")}
        </select>
      </td>
      <td>
        <button class="btn btn-sm ${item.estado ? 'btn-success' : 'btn-danger'} btn-estado"
          data-id="${item.id}"
          title="${item.estado ? 'Desactivar' : 'Activar'}">
          <i class="fas ${item.estado ? 'fa-toggle-on' : 'fa-toggle-off'}"></i>
        </button>
        <button class="btn btn-sm btn-primary guardar-fila" data-id="${item.id}">
          <i class="fas fa-save"></i>
        </button>
        <button class="btn btn-sm btn-warning" onclick="abrirModal(${item.id})">
          <i class="fas fa-pen"></i>
        </button>
      </td>
    </tr>
  `);
  $("#tableBody").html(rows.join(""));
}

function cambiarEstado(id, nuevoEstado) {
  const url = `empresa/${id}`;
  const empresa = { estado: !!nuevoEstado };

  callApi("PUT", url, empresa)
    .done(function (response) {
      if (response.respuesta) {
        const row = $(`button.guardar-fila[data-id="${id}"]`).closest("tr");
        const btn = row.find(".btn-estado");
        const icon = btn.find("i");

        btn
          .removeClass("btn-success btn-danger")
          .addClass(nuevoEstado ? "btn-success" : "btn-danger")
          .attr("title", nuevoEstado ? "Desactivar" : "Activar");

        icon
          .removeClass("fa-toggle-on fa-toggle-off")
          .addClass(nuevoEstado ? "fa-toggle-on" : "fa-toggle-off");

        showInfo("Estado actualizado correctamente");
      } else {
        showWarning("No se pudo actualizar el estado");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

function abrirModal(id = null) {
  if (id) {
    const urls = [`empresa/${id}`, `empresa/lista-usuarios-empresa/${id}`];
    fetchMultiple(
      urls,
      function (responses) {
        const [empresas, usuarios] = responses.map(r => (r.respuesta ? r.data : []));
        const emp = empresas;

        if (emp) {
          $("#empresaId").val(emp.id);
          $("#nombre").val(emp.nombre);
          $("#tipoEmpresa").val(emp.id_tipo_empresa);
          $("#estado").prop("checked", emp.estado);
          cargarModulos();
        }

        if (usuarios && Array.isArray(usuarios)) {
          cargarUsuarios(usuarios);
        }

        $('#empresaTabs button[data-bs-target="#datos"]').tab('show');
        $("#modalEmpresa").modal("show");
      },
      function (err) {
        console.error("Fallo global:", err);
      }
    );
  } else {
    $("#formEmpresa")[0].reset();
    $("#empresaId").val("");
    $("#modalEmpresa").modal("show");
  }
}

async function cargarModulos() {
  $("#modulosContainer").empty();
  const empresaId = $("#empresaId").val();
  if (empresaId) {
    const data = await getEmpresaModulo(empresaId);
    modulos.forEach(modulo => {
      const checked = data.find(item => item.id_modulo === modulo.id && item.estado === true)
        ? "checked" : "";
      const html = `
        <div class="col-md-6">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" name="modulos"
              value="${modulo.id}" id="modulo-${modulo.id}" ${checked}>
            <label class="form-check-label" for="modulo-${modulo.id}">${modulo.nombre}</label>
          </div>
        </div>
      `;
      $("#modulosContainer").append(html);
    });
  }
}

async function cargarUsuarios(data) {
  console.log("Usuarios recibidos:", data);

  const $container = $("#usuariosContainer");
  $container.empty(); // Limpia el contenedor

  if (!Array.isArray(data) || data.length === 0) {
    $container.html('<div class="alert alert-warning">Sin usuarios asociados a esta empresa.</div>');
    return;
  }

  // Construcción de tabla si hay usuarios
  let html = `
    <table class="table table-sm table-bordered table-striped">
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Perfiles</th>
        </tr>
      </thead>
      <tbody>
  `;

  data.forEach(usuario => {
    html += `
      <tr>
        <td>${usuario.username || '-'}</td>
        <td>${usuario.perfiles || '-'}</td>
      </tr>
    `;
  });

  html += `
      </tbody>
    </table>
  `;

  $container.html(html);
}
   

async function getEmpresaModulo(empresa) {
  try {
    const response = await callApi('GET', `empresamodulo/empresa/${empresa}`);
    if (!response.respuesta) {
      showWarning("No se pudo cargar usuarios");
      return [];
    }
    return response.data;
  } catch (err) {
    showDanger("No se puede conectar con el servidor");
    return [];
  }
}

function guardarEmpresa(empresaData = null, empresaId = null) {
  const id = empresaId ?? $("#empresaId").val();
  const empresa = empresaData ?? {
    nombre: $("#nombre").val(),
    id_tipo_empresa: parseInt($("#tipoEmpresa").val()),
    estado: $("#estado").is(":checked"),
  };
  const url = id ? `empresa/${id}` : "empresa";
  const method = id ? "PUT" : "POST";

  callApi(method, url, empresa)
    .done(function (response) {
      if (response.respuesta) {
        guardarModulos();
        showInfo("Cambios correctamente guardados");
        $("#modalEmpresa").modal("hide");
        cargarConsultas();
      } else {
        showWarning("No se puede guardar la información");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

function guardarModulos() {
  const modulosSeleccionados = [];
  $("#modulosContainer input[type='checkbox']").each(function () {
    modulosSeleccionados.push({
      id_modulo: $(this).val(),
      estado: $(this).is(":checked"),
    });
  });
  const param = { id_empresa: $("#empresaId").val(), modulos: modulosSeleccionados };
  callApi("POST", "empresamodulo/guardar-relacion", param)
    .done(function (response) {
      // éxito / manejo si se desea
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

$(document)
  .off("click", ".guardar-fila")
  .on("click", ".guardar-fila", function () {
    const id = $(this).data("id");
    const row = $(this).closest("tr");
    const nombre = row.find("input").val();
    const id_tipo_empresa = row.find("select").val();
    const empresa = {
      nombre,
      id_tipo_empresa: parseInt(id_tipo_empresa),
    };
    guardarEmpresa(empresa, id);
  });
