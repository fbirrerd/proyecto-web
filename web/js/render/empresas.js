let currentData = [],
    tipoEmpresas = [],
    modulos = [],
    modulosSeleccionados = [];

$(document).ready(() => {
  cargarConsultas();
  //   cargarEmpresas();

  $("#formEmpresa").submit(function (e) {
    e.preventDefault();
    guardarEmpresa();
  });
});

function cargarConsultas() {
  const urls = ["empresa", "tipoempresa/list/all","modulo"];

  fetchMultiple(
    urls,
    function (responses) {
      [currentData, tipoEmpresas, modulos] = responses.map((r) =>
        r.respuesta ? r.data : []
      );
      cargarEmpresas();
      cargarTiposEmpresa();
      cargarModulos();
    },
    function (err) {
      console.error("Fallo global:", err);
    },
  );
}

function cargarTiposEmpresa() {
  $("#tipoEmpresa").html(
    '<option value="">Seleccione</option>' +
      tipoEmpresas
        .map((t) => `<option value="${t.id}">${t.nombre}</option>`)
        .join("")
  );
}

function cargarEmpresas() {
  const rows = currentData.map(
    (emp) => `
      <tr>
        <td><input class="form-control form-control-sm" value="${
          emp.nombre
        }" onchange="editarCampo(${emp.id}, 'nombre', this.value)"></td>
        <td>
          <select class="form-select form-select-sm" onchange="editarCampo(${
            emp.id
          }, 'id_tipo_empresa', this.value)">
            ${tipoEmpresas
              .map(
                (t) =>
                  `<option value="${t.id}" ${
                    t.id === emp.id_tipo_empresa ? "selected" : ""
                  }>${t.nombre}</option>`
              )
              .join("")}
          </select>
        </td>
        <td>
            <button class="btn btn-sm toggle-estado ${emp.estado ? "btn-success" : "btn-secondary"}" 
            data-id="${emp.id}"onclick="cambiarEstado(${emp.id}, ${!emp.estado})">
                ${emp.estado ? "Activo" : "Inactivo"}
            </button>
            <button class="btn btn-sm btn-primary guardar-fila" data-id="${emp.id}">
                <i class="fas fa-save"></i> 
            </button>
            <button class="btn btn-sm btn-warning" onclick="abrirModal(${
              emp.id
            })">
                <i class="fas fa-pen"></i> 
            </button>        
        </td>
      </tr>
    `
  );
  $("#tableBodyEmpresa").html(rows.join(""));
}

function cambiarEstado(id, nuevoEstado) {
  const url = [`empresa/${id}`];

  const empresa = {
    estado: nuevoEstado,
  };

  let resultado = callApi("PUT", url, empresa)
    .done(function (response) {
      if (response.respuesta) {
        const btn = $(`button.toggle-estado[data-id="${id}"]`);
        btn
          .toggleClass("btn-success", nuevoEstado)
          .toggleClass("btn-secondary", !nuevoEstado)
          .text(nuevoEstado ? "Activo" : "Inactivo")
          .attr("onclick", `cambiarEstado(${id}, ${!nuevoEstado})`);
        showInfo("Cambios correctamente guardados");
      } else {
        showWarning("no se puede traer la información de menus");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

function abrirModal(id = null) {
  if (id) {
    const urls = [`empresa/${id}`];
    fetchMultiple(
      urls,
      function (responses) {
        const [emp] = responses.map((r) => (r.respuesta ? r.data : []));
        if (emp) {
          $("#empresaId").val(emp.id);
          $("#nombre").val(emp.nombre);
          $("#tipoEmpresa").val(emp.id_tipo_empresa);
          $("#estado").prop("checked", emp.estado);
          cargarModulos();
        }
        $("#modalEmpresa").modal("show");
      },
      function (err) {
        console.error("Fallo global:", err);
      }
    );
  } else {
    // 👉 Aquí está la parte que faltaba
    $("#formEmpresa")[0].reset();
    $("#empresaId").val("");
    $("#modalEmpresa").modal("show");
  }
};


async function cargarModulos(){
  
  $("#modulosContainer").empty();
    if($("#empresaId").val()){
      const data = await getEmpresaModulo($("#empresaId").val());
      console.log(data);
      modulos.forEach(function (modulo) {
        const checked =  data.find(item => item.id_modulo === modulo.id && item.estado === true) ? "checked" : "";

        const html = `
          <div class="col-md-6">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="modulos" value="${modulo.id}" id="modulo-${modulo.id}" ${checked}>
              <label class="form-check-label" for="modulo-${modulo.id}">${modulo.nombre}</label>
            </div>
          </div>
        `;
        $("#modulosContainer").append(html);
      });
    }
};

async function getEmpresaModulo(empresa){
  let datos = [];
  await callApi('GET', `empresamodulo/empresa/${empresa}`, undefined)
    .done(function(response) {
        datos = response.data;
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor");          
    });
    return datos;
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
        guardarModulos()
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

function guardarModulos(){
  const modulosSeleccionados = [];

  $("#modulosContainer input[type='checkbox']").each(function () {
    modulosSeleccionados.push({
      id_modulo: $(this).val(),
      estado: $(this).is(":checked"),
    });
  });

  let param = {
    id_empresa: $("#empresaId").val(),
    modulos: modulosSeleccionados
  };
  console.log("guardar", param);

  callApi("POST", "empresamodulo/guardar-relacion", param)
    .done(function (response) {
      console.log(response)
      if (response.respuesta) {

      } else {

      }
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
      // el estado no se modifica aquí
    };

    guardarEmpresa(empresa, id);
  });
