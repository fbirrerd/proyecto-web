let currentData = [];

function cargarTipos() {
  let params;
  callApi('GET', 'tipoempresa', params)
    .done(function(response) {
          if (response.respuesta) {
            currentData = response.data;
            llenarTabla();
            
          } else {
            showWarning("Error al cargar tipos de empresa");
          }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });


}

function llenarTabla() {
  const $tbody = $("#tableBody").empty();

  currentData.forEach((item) => {
    const $row = $(`
      <tr data-id="${item.id}">
        <td>
          <input class="form-control form-control-sm nombre" value="${item.nombre}">
        </td>
        <td class="acciones-td  text-end">
          <button 
            class="btn btn-sm ${item.estado ? 'btn-success' : 'btn-danger'} btn-estado" 
            data-id="${item.id}"
            title="${item.estado ? 'Desactivar' : 'Activar'}"
          >
            <i class="fas ${item.estado ? 'fa-toggle-on' : 'fa-toggle-off'}"></i>
          </button>
          <button class="btn btn-sm btn-success me-1 btn-guardar" data-id="${item.id}">
            <i class="fas fa-save"></i>
          </button>
          <button class="btn btn-sm btn-warning me-1 btn-editar" data-id="${item.id}">
            <i class="fas fa-edit"></i>
          </button>
        </td>
      </tr>
    `);

    $tbody.append($row);
  });
}

$(document).on('click', '.btn-editar', function () {
  const id = $(this).data('id');
  const item = currentData.find(i => i.id === id);

  // Guardamos el ID en el botón para luego usarlo
  
  $('#btnGuardarCambios').data('id', id);
  $('#inputNombreEditar').val(item.nombre);
  $('#inputEstadoEditar').val(item.estado.toString());
  verEmpresas(id);
  // Mostramos el modal
  const modal = new bootstrap.Modal(document.getElementById('modalEditar'));
  modal.show();
});


$("#formTipoEmpresa").on("submit", function (e) {
  e.preventDefault();

  const nombre = this.nombre.value.trim();
  const estado = this.estado.value === "true";

  if (!nombre) {
    alert("Debe ingresar un nombre");
    return;
  }

  $.ajax({
    url: apiUrl,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ nombre, estado }),
    success: () => {
      $("#modalTipoEmpresa").modal("hide");
      this.reset();
      cargarTipos();
    },
    error: () => {
      alert("Error al guardar");
    },
  });
});

$("#tableBody").on("click", ".btn-guardar", function () {
  const row = $(this).closest("tr");
  const id = row.data("id");
  const nombre = row.find(".nombre").val().trim();

  const params = {
    nombre: nombre
  }

  callApi('PUT', `tipoempresa/${id}`, params)
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
  const nombre = row.find(".nombre").val().trim();
  const estadoActual = $(this).hasClass("btn-success");


  const params = {
    estado: !estadoActual
  }

  callApi('PUT', `tipoempresa/${id}`, params)
    .done(function(response) {
          if (response.respuesta) {
            cargarTipos();
          } else {
            showWarning("Error al guardar tipos de empresa");
          }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });
});

function verEmpresas(tipo) {
  console.log(tipo);

  // Llamada a la API con tipo en la URL directamente
  callApi('GET', `tipoempresa/empresas/${tipo}`)
    .done(function(response) {
      $("#empresasTipoList").empty(); // Limpiar lista

      if (response.respuesta && Array.isArray(response.data)) {
        if (response.data.length === 0) {
          // Mostrar mensaje si no hay empresas asociadas
          const $msg = $("<li>")
            .addClass("list-group-item bg-warning text-dark")
            .text("No está asociada a ninguna empresa.");
          $("#empresasTipoList").append($msg);
        } else {
          // Mostrar las empresas
          $.each(response.data, function(index, empresa) {
            const $li = $("<li>")
              .addClass("list-group-item")
              .html(`${empresa.nombre}`);
            $("#empresasTipoList").append($li);
          });
        }
      } else {
        showWarning("No fue posible obtener las empresas asociadas.");
      }
    })
    .fail(function() {
      showDanger("No se pudo conectar con el servido  r.");
    });
}


$(document).ready(() => {
  cargarTipos();
});


$('#btnNuevo').on('click', function () {
  const $tbody = $("#tableBody");

  const $nuevaFila = $(`
    <tr class="nueva-fila">
      <td>
        <input type="text" class="form-control form-control-sm nombre" placeholder="Nombre del tipo de empresa">
      </td>
      <td class="acciones-td  text-end">
        <button class="btn btn-sm btn-success btn-guardar-nuevo me-2"><i class="fas fa-save"></i></button>
        <button class="btn btn-sm btn-secondary btn-cancelar-nuevo"><i class="fas fa-times"></i></button>
      </td>
    </tr>
  `);

  $tbody.prepend($nuevaFila); // Agrega arriba de la tabla
});


// Guardar nuevo registro
$(document).on('click', '.btn-guardar-nuevo', function () {
  const $fila = $(this).closest('tr');
  const nombre = $fila.find('.nombre').val().trim();

  if (!nombre) {
    alert('El nombre no puede estar vacío.');
    return;
  }

  const params = {
    nombre: nombre,
    estado: true
  };

  callApi('POST', 'tipoempresa', params)
    .done(function(response) {
          if (response.respuesta) {
            cargarTipos();
          } else {
            showWarning("Error al guardar tipos de empresa");
          }
    })
    .fail(function() {
        showDanger("No se puede conectar con el servidor"); 
    });


});

// Cancelar creación
$(document).on('click', '.btn-cancelar-nuevo', function () {
  $(this).closest('tr').remove();
});
