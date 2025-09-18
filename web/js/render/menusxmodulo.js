let currentData = [];
let editModal;

document.addEventListener("DOMContentLoaded", () => {
  fetchitems();
  editModal = new bootstrap.Modal(document.getElementById("editModal"));
  document
    .getElementById("editForm")
    .addEventListener("submit", guardarCambios);
});

function fetchitems() {
  const params = {
    id_tipo_menu: 2,
    solo_activos: false,
    ordenado: true
  };

  callApi("POST", "menu/modulos", params)
    .done(function (response) {
      if (response.respuesta) {
        currentData = response.data;
        llenarTabla();
      } else {
        showWarning("Error al cargar el menu");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
}

const tipoOptions = ["link", "padre", "blank", "popup"];

function llenarTabla() {
  const $tbody = $("#tableBody");
  $tbody.empty();
  currentData.forEach((item) => {
    const $row = $("<tr>");

    // Div que simula el select para los iconos
    let icon = item.icono;
    let iconObj = iconosFontAwesome.find((i) => i.icon === icon);

    // Si no tiene ícono seleccionado, usar texto "Seleccione"
    let dropdownBtnContent = iconObj
      ? `<i class="${iconObj.icon} me-2"></i> <span class="icon-name">${iconObj.name}</span>`
      : `<span class="text-muted icon-name">Seleccione</span>`;

    let $iconSelectDiv = $(`
          <div class="dropdown">
            <button class="btn dropdown-toggle btn-sm" type="button" id="dropdown-${
              item.id
            }" data-bs-toggle="dropdown" aria-expanded="false">
              ${dropdownBtnContent}
            </button>
            <ul class="dropdown-menu dropdown-menu-sm dropdown-menu-scrollable" aria-labelledby="dropdown-${
              item.id
            }">
              ${iconosFontAwesome
                .map(
                  (iconObj) => `
                <li>
                  <a class="dropdown-item icon-item" href="#"
                    data-icon="${iconObj.icon}"
                    data-name="${iconObj.name}"
                    data-id="${item.id}">
                    <i class="${iconObj.icon} me-2"></i> ${iconObj.name}
                  </a>
                </li>
              `
                )
                .join("")}
            </ul>
          </div>
          <input type="hidden" id="icono-${item.id}" value="${icon || ""}">
        `);

    // Agregar el resto de campos de la tabla
    $row.append(
      $("<td>").append($iconSelectDiv),
      $("<td>").append(
        `<input type="text" class="form-control form-control-sm small-input" id="nombre-${item.id}" value="${item.nombre}">`
      ),
      $("<td>").append(
        `<input type="text" class="form-control form-control-sm small-input" id="ruta-${
          item.id
        }" value="${item.url ?? ""}">`
      ),
      // $("<td>").append(`<select class="form-select form-select-sm small-input" id="tipo-${item.id}">
      //     ${tipoOptions.map(tipo => `<option value="${tipo}" ${tipo === item.tipo ? "selected" : ""}>${tipo}</option>`).join('')}
      // </select>`),
      $("<td>").append(`
                <select class="form-select form-select-sm small-input" id="padre-${
                  item.id
                }">>
                    <option value="">-- Sin padre --</option>
                    ${currentData // solo padres
                      .map(
                        (padre) => `
                            <option value="${padre.id}" ${
                          padre.id === item.id_padre ? "selected" : ""
                        }>
                                ${padre.nombre}
                            </option>
                        `
                      )
                      .join("")}
                </select>
            `),
      // $("<td>").append(`<input type="number" class="form-control form-control-sm" style="width:50px" id="orden-${item.id}" value="${item.orden}">`),
      $("<td class='acciones  text-end'>").append(`
                <button class="btn btn-sm ${
                  item.estado ? "btn-success" : "btn-danger"
                } btn-estado" 
                    data-id="${item.id}" title="${
        item.estado ? "Desactivar" : "Activar"
      }">
                    <i class="fas ${
                      item.estado ? "fa-toggle-on" : "fa-toggle-off"
                    }"></i>
                </button>                
                <button class="btn btn-success btn-sm guardar-btn " data-id="${
                  item.id
                }">
                    <i class="fas fa-save"></i>
                </button>
                <button class="btn btn-sm btn-warning" onclick="abrirModalEditar(${
                  item.id
                })">
                    <i class="fas fa-edit"></i>
                </button>
            `)
    );

    $tbody.append($row);
  });
}

$("#tableBody").on("click", ".btn-estado", function () {
  const id = $(this).data("id");
  const row = $(this).closest("tr");
  const estadoActual = $(this).hasClass("btn-success");

  const isActivo = this.classList.contains("btn-success");

  // Alternar clases
  this.classList.toggle("btn-success", !isActivo);
  this.classList.toggle("btn-danger", isActivo);

  // Cambiar título
  this.title = isActivo ? "Activar" : "Desactivar";

  const params = {
    id: id,
    estado: !estadoActual,
  };

  callApi("PUT", "menu/cambiar-estado", params)
    .done(function (response) {
      if (response.respuesta) {
        showInfo("Estado actualizado con exito");
      } else {
        showWarning("Hubo un error al intentar actualizar");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
});

// 🟢 GUARDAR cambios desde la fila
$(document).on("click", ".guardar-btn", function () {
  const id = $(this).data("id");

  const params = {
    id: id,
    nombre: $(`#nombre-${id}`).val(),
    icono: $(`#icono-${id}`).val(),
    url: $(`#ruta-${id}`).val(),
    id_padre: $(`#padre-${id}`).val() || null, // Si está vacío, usa null
  };

  callApi("PUT", "menu/generales", params)
    .done(function (response) {
      if (response.respuesta) {
        showInfo("Estado actualizado con exito");
        fetchitems();
      } else {
        showWarning("Hubo un error al intentar actualizar");
      }
    })
    .fail(function () {
      showDanger("No se puede conectar con el servidor");
    });
});

// Asignar icono al seleccionar una opción
$(document).on("click", ".icon-item", function (e) {
  e.preventDefault();

  const newIcon = $(this).data("icon");
  const newName = $(this).data("name");
  const itemId = $(this).data("id");

  const $btn = $(`#dropdown-${itemId}`);

  // Reemplaza el icono
  $btn.find("i").attr("class", `${newIcon} me-2`);

  // Reemplaza el texto por el name (más corto)
  $btn.find(".icon-name").text(newName);

  // Guarda en el input hidden el valor completo del icono
  $(`#icono-${itemId}`).val(newIcon);
});

// ✏️ ABRIR MODAL para edición completa

// $(document).on("click", ".editar-btn", function () {
//     const id = $(this).data("id");
//     const item = currentData.find(r => r.id === id);

//     if (!item) return;

//     const $iconoSelect = $("#icono-select");
//     $iconoSelect.empty(); // limpiar opciones previas
//     iconosFontAwesome.forEach(icon => {
//         const selected = icon === item.icono ? 'selected' : '';
//         $iconoSelect.append(`
//             <option value="${icon}">
//                 ${icon}
//             </option>
//         `);
//     });

//     // 🔽 Llenar select de menús padre
//     const $itemPadreSelect = $("#padre-select");
//     $itemPadreSelect.empty();i
//     $itemPadreSelect.append(`<option value="">(Sin padre)</option>`); // opción vacía

//     currentData.forEach(m => {
//         // Evitar que un menú sea su propio padre
//         if (m.id !== id) {
//             const selected = m.id === item.id_padre ? "selected" : "";
//             $itemPadreSelect.append(
//                 `<option value="${m.id}" ${selected}>${m.nombre}</option>`
//             );
//         }
//     });

//     // Cargar datos en el modal
//     // $("#editForm [name='id']").val(item.id);
//     // $("#editForm [name='nombre']").val(item.nombre);
//     // $("#editForm [name='ruta']").val(item.ruta);
//     // $("#editForm [name='id_padre']").val(item.id_padre);
//     // $("#editForm [name='tipo']").val(item.tipo);
//     // $("#editForm [name='orden']").val(item.orden);
//     // $("#editForm [name='estado']").val(item.estado.toString());

//     // Mostrar el modal
//     const modal = new bootstrap.Modal(document.getElementById("editModal"));
//     modal.show();
// });

// Esta función se ejecuta cuando haces clic en el botón de editar
async function abrirModalEditar(menuId) {
  // Obtener los datos del menú por ID desde tu API
  const resMenu = await fetch(`/api/menus/${menuId}`);
  const menu = await resMenu.json();

  // Obtener la lista completa de roles
  const resRoles = await fetch("/api/roles");
  const roles = await resRoles.json();

  // Obtener los roles asociados a este menú
  const resRolesAsociados = await fetch(`/api/menus/${menuId}/roles`);
  const rolesAsociados = await resRolesAsociados.json();
  const rolesSeleccionados = rolesAsociados.map((r) => r.id); // [1, 2, ...]

  // Llenar los campos del formulario
  document.getElementById("menu-id").value = menu.id;
  document.getElementById("nombre").value = menu.nombre;
  document.getElementById("ruta").value = menu.ruta;
  document.getElementById("orden").value = menu.orden;
  document.getElementById("estado").value = menu.estado;

  // Selects (rellénalos si no están llenos aún)
  await cargarSelects(); // Función que llena los select de iconos, padres y tipos si es necesario

  document.getElementById("icono-select").value = menu.icono;
  document.getElementById("padre-select").value = menu.id_padre || "";
  document.getElementById("tipo-select").value = menu.id_tipo_menu;

  // Llenar checkboxes de roles
  const rolesContainer = document.getElementById("roles-container");
  rolesContainer.innerHTML = ""; // Limpiar primero

  roles.forEach((rol) => {
    const checked = rolesSeleccionados.includes(rol.id) ? "checked" : "";
    const div = document.createElement("div");
    div.className = "form-check";
    div.innerHTML = `
        <input class="form-check-input" type="checkbox" name="roles" id="rol-${rol.id}" value="${rol.id}" ${checked}>
        <label class="form-check-label" for="rol-${rol.id}">${rol.nombre}</label>
      `;
    rolesContainer.appendChild(div);
  });

  // Abrir el modal
  const modal = new bootstrap.Modal(document.getElementById("editModal"));
  modal.show();
}

function editar(id) {
  const item = currentData.find((m) => m.id === id);
  if (!item) return;

  const form = document.getElementById("editForm");
  for (let key in item) {
    if (form[key] !== undefined) {
      form[key].value = item[key];
    }
  }
  editModal.show();
}

function guardarCambios(e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  data.id = parseInt(data.id);
  data.orden = parseInt(data.orden);
  data.estado = data.estado === "true";
  data.es_publico = false;
  data.icono = "";
  data.fecha_creacion = new Date().toISOString();
  data.fecha_modificacion = new Date().toISOString();

  fetch("/item", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then(() => {
      editModal.hide();
      $("#filtroGeneral").val("");
      fetchitems();
    });
}

// Mostrar modal en modo "crear"
function mostrarFilaNueva() {
  limpiarFormulario();
  $("#editModalLabel").text("Crear Menú");
  const modal = new bootstrap.Modal(document.getElementById("editModal"));
  modal.show();
}

// Mostrar modal en modo "editar"
function editarMenu(menu) {
  $("#editModalLabel").text("Editar Menú");
  $("#menu-id").val(menu.id);
  $("#nombre").val(menu.nombre);
  $("#icono").val(menu.icono);
  $("#url").val(menu.url);
  $("#descripcion").val(menu.descripcion);
  $("#id_tipo_menu").val(menu.id_tipo_menu);
  $("#id_padre").val(menu.id_padre);
  $("#orden").val(menu.orden);
  $("#estado").val(menu.estado.toString());

  const modal = new bootstrap.Modal(document.getElementById("editModal"));
  modal.show();
}

// Limpiar el formulario
function limpiarFormulario() {
  $("#editForm")[0].reset();
  $("#menu-id").val("");
}

function normalizarTexto(texto) {
    return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function aplicarFiltroTabla() {
    const filtro = normalizarTexto($("#filtroGeneral").val());

    $("#tableBody tr").each(function () {
        const fila = $(this);
        let textoFila = "";

        // Excluir la primera celda (índice 0)
        fila.find("td").each(function (index) {
            if (index === 0 || index === 3  ) return; // omitir la primera td

            const celda = $(this);
            // console.log(celda.text())

            textoFila += " " + normalizarTexto(celda.text());

            celda.find("input, select").each(function () {
                textoFila += " " + normalizarTexto($(this).val() || "");
            });

            celda.find(".dropdown-toggle .icon-name").each(function () {
                textoFila += " " + normalizarTexto($(this).text());
            });
        });

        fila.toggle(textoFila.includes(filtro));
    });
}

// Eventos de filtro en tiempo real
$("#filtroGeneral").on("keyup input", aplicarFiltroTabla);

// Botón para limpiar
$("#limpiarFiltro").click(function () {
    $("#filtroGeneral").val("").trigger("input");
});