

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
    await fetchMenus(); 


    let html = '<table class="table table-striped mt-3"><thead><tr><th>Menú</th>';
    roles.forEach(role => {
      html += `<th class="vertical-text" style="
    writing-mode: vertical-rl; text-align: center;
    vertical-align: middle;">${role.nombre}</th>`;
    });
    html += '</tr></thead><tbody>';

    menus.forEach(menu => {

      let icon = '  <i class="fa-solid fa-arrow-right"></i>'.repeat(menu.nivel);

      html += `<tr><td class="text-start">${icon} ${menu.nombre}</td>`;
      roles.forEach(role => {
        const match = data.find(d => d.id_menu === menu.id && d.id_rol === role.id);
        const checked = match?.estado ? "checked" : "";
        const icon = match?.estado ? 'fa-check-circle' : 'fa-times-circle';
        html += `<td class="checkbox-wrapper">
                  <input type="checkbox" class="permiso" data-menu="${menu.id}" data-rol="${role.id}" ${checked}>
                </td>`;
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    $('#tableContainer').html(html);
  }

    // Evento para armar datos y enviar a la API
    $('#guardarCambios').click(async function () {
      const relaciones = [];

      $('.permiso').each(function () {
        const menuId = $(this).data("menu");
        const rolId = $(this).data("rol");
        const estado = $(this).is(":checked");

        relaciones.push({
          id_menu: menuId,
          id_rol: rolId,
          estado: estado
        });
      });

      await callApi('POST', 'rolmenu/guardar-relaciones', {relaciones: relaciones})
      .done(function(response) {
        if(response.respuesta){
          showInfo("Cambios correctamente guardados"); 
        }else{
          showWarning("no se puede traer la información de menus"); 
        }
      })
      .fail(function() {
          showDanger("No se puede conectar con el servidor"); 
      });

    });

    $(document).ready(buildTable);

    console.log("rolmenu.js cargado (versión con jQuery para UI).");
