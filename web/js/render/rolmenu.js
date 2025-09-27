

let menus = []
let roles = []
let datos = [] 
let params

async function fetchMenus() {

  await callApi('GET', 'menu/generales', params)
  .done(function(response) {
    if(response.respuesta){
      menus = response.data;
    }else{
      showWarning("No se puede traer la información de menus"); 
    }
  })
  .fail(function() {
      showDanger("No se puede conectar con el servidor"); 
  });

  await callApi('GET', 'rol', params)
  .done(function(response) {
    if(response.respuesta){
      roles = response.data;
    }else{
      showWarning("no se puede traer la información de roles"); 
    }
  })
  .fail(function() {
      showDanger("No se puede conectar con el servidor"); 
  });

  await callApi('GET', 'rolmenu', params)
  .done(function(response) {
    if(response.respuesta){
      data = response.data;
    }else{
      showWarning("no se puede traer la información de roles"); 
    }
  })
  .fail(function() {
      showDanger("No se puede conectar con el servidor"); 
  });

}

async function buildTable() {
  try {
    await fetchMenus();
  } catch (error) {
    console.error("Error al cargar los menús:", error);
    $('#tableContainer').html('<p>Error al cargar la tabla.</p>');
    return;
  }

  let html = `
    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th>Menú</th>
  `;

  // Encabezado con íconos para seleccionar todos
  roles.forEach(role => {
    html += `
      <th class="vertical-text text-center">
        <div style="writing-mode: vertical-rl; text-align: center;">
          <i class="fas fa-toggle-off toggle-all"
             data-rol="${role.id}" 
             style="cursor: pointer; font-size: 20px;"></i>
          <div>${role.nombre}</div>
        </div>
      </th>
    `;
  });

  html += `</tr></thead><tbody>`;

  menus.forEach(menu => {
    let icon = '<i class="fa-solid fa-arrow-right"></i>'.repeat(menu.nivel);
    html += `<tr><td class="text-start">${icon} ${menu.nombre}</td>`;

    roles.forEach(role => {
      const match = data.find(d => d.id_menu === menu.id && d.id_rol === role.id);
      const isActive = match?.estado;  // Asignamos el valor del estado
      const iconClass = isActive ? 'fa-toggle-on text-success' : 'fa-toggle-off text-danger';

      html += `
        <td class="text-center">
          <i class="fas ${iconClass} permiso toggle-r${role.id}" 
             data-menu="${menu.id}" data-rol="${role.id}" 
             style="cursor: pointer; font-size: 18px;"></i>
        </td>
      `;
    });

    html += '</tr>';
  });

  html += '</tbody></table>';
  $('#tableContainer').html(html);

  // Después de cargar la tabla, actualizamos los íconos del encabezado
  updateHeaderIcons();

  // ✅ Toggle individual
  $('.permiso').on('click', function () {
    const $icon = $(this);
    const rolId = $icon.data('rol');

    const isOn = $icon.hasClass('fa-toggle-on');
    $icon.toggleClass('fa-toggle-on text-success', !isOn)
         .toggleClass('fa-toggle-off text-danger', isOn);

    updateColumnHeaderIcon(rolId);
  });

  // ✅ Toggle por columna
  $('.toggle-all').on('click', function () {
    const $icon = $(this);
    const rolId = $icon.data('rol');
    const icons = $(`.toggle-r${rolId}`);

    // Contar estados actuales
    const countOn = icons.filter('.fa-toggle-on').length;
    const countOff = icons.length - countOn;

    let newState;
    if (countOn === icons.length) {
      newState = 'off'; // si todos estaban activos, apágalos
    } else {
      newState = 'on'; // si hay mezcla o todos apagados, enciéndelos
    }

    icons.each(function () {
      const $i = $(this);
      $i.toggleClass('fa-toggle-on text-success', newState === 'on')
        .toggleClass('fa-toggle-off text-danger', newState === 'off');
    });

    updateColumnHeaderIcon(rolId);
  });

  // ✅ Actualiza ícono de encabezado según estados de columna
  function updateColumnHeaderIcon(rolId) {
    const icons = $(`.toggle-r${rolId}`);
    const headerIcon = $(`.toggle-all[data-rol="${rolId}"]`);
    const countOn = icons.filter('.fa-toggle-on').length;
    const countOff = icons.length - countOn;

    if (countOn === icons.length) {
      headerIcon.removeClass().addClass('fas fa-toggle-on text-success toggle-all');
    } else if (countOff === icons.length) {
      headerIcon.removeClass().addClass('fas fa-toggle-off text-danger toggle-all');
    } else {
      headerIcon.removeClass().addClass('fas fa-adjust text-warning toggle-all');
    }
  }

  // Actualiza los íconos del encabezado según el estado inicial de los íconos de las filas
  function updateHeaderIcons() {
    roles.forEach(role => {
      const icons = $(`.toggle-r${role.id}`);
      const headerIcon = $(`.toggle-all[data-rol="${role.id}"]`);
      const countOn = icons.filter('.fa-toggle-on').length;
      const countOff = icons.length - countOn;

      if (countOn === icons.length) {
        headerIcon.removeClass().addClass('fas fa-toggle-on text-success toggle-all');
      } else if (countOff === icons.length) {
        headerIcon.removeClass().addClass('fas fa-toggle-off text-danger toggle-all');
      } else {
        headerIcon.removeClass().addClass('fas fa-adjust text-warning toggle-all');
      }
    });
  }
}



    // Evento para armar datos y enviar a la API
$('#guardarCambios').click(async function () {
  const relaciones = [];

  // Recorre todos los íconos de permisos (toggle)
  $('.permiso').each(function () {
    const menuId = $(this).data("menu");
    const rolId = $(this).data("rol");

    // Verifica si el ícono tiene la clase 'fa-toggle-on' para determinar si está activo
    const estado = $(this).hasClass('fa-toggle-on');  // Si tiene 'fa-toggle-on', está activo

    relaciones.push({
      id_menu: menuId,
      id_rol: rolId,
      estado: estado
    });
  });

  // Realiza la solicitud POST para guardar las relaciones
  await callApi('POST', 'rolmenu/guardar-relaciones', { relaciones: relaciones })
  .done(function(response) {
    if (response.respuesta) {
      showInfo("Cambios correctamente guardados");
    } else {
      showWarning("No se pudo guardar la información de menús");
    }
  })
  .fail(function() {
    showDanger("No se puede conectar con el servidor");
  });
});


    $(document).ready(buildTable);

    console.log("rolmenu.js cargado (versión con jQuery para UI).");
