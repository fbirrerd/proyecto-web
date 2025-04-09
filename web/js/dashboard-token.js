$(document).ready(function () {

    function getDatos() {
        let cadena = localStorage.getItem('dataSystem')
        let data = JSON.parse(cadena);
        return data;
    }

    let data = getDatos();
    if (data) {
        let tokenData = data;

        // Si 'token' existe en el objeto, accedemos a él
        let token = tokenData.token;
        let empresas = tokenData.empresas;
        LoadEmpresas(empresas)
        IniciarMenu(tokenData);
      
    } else {
        console.log('No token found in localStorage');
    }





    function LoadEmpresas(empresasJSON) {
        const dropdownMenu = document.querySelector('.dropdown-menu');
    
        // Limpiar el contenido inicial del dropdown (opcional)
        dropdownMenu.innerHTML = '';
   
        if (empresasJSON.length > 0) {
            cargarNombreEmpresa(empresasJSON[0].nombre);
        } else {
            console.log("No hay empresas en el JSON.");
        }
    
        // Cargar empresas en el dropdown
        const companyList = $("#companyList");
        empresasJSON.forEach(emp => {
            companyList.append(`
                <li><a class="dropdown-item empresa-opcion" href="#" data-id="${emp.id}">${emp.nombre}</a></li>
            `);
        });

    }
    

})

function cargarNombreEmpresa(empresaNombre){
    $("#companyDropdown").html(`<i class="fas fa-building fa-fw me-1"></i> ${empresaNombre}`);
}

function IniciarMenu(tokenData){
    LoadMenu(tokenData.menusGenerales, "leftMenuGeneralContainer")
    // LoadMenu(tokenData.menusEspecificos, "leftMenuEspecificoContainer")
}
function LoadMenu(menuJson, idContainer) {
    console.log("loadMenu")    
    let datos = getHijosOrdenados(menuJson, null);

    console.log("datos Filtrados y Ordenados", datos);

    let menuHTML = `<ul class="list-unstyled components mb-5">`;
    let strPadre = "";
    datos.forEach(nodo => {
        let identificadorMenuHijo = "";
        let sTarget = ``;
        let link = `href="${nodo.ruta}" target="main-iframe" class="menu-link"`
        let sCaption = `<i class="${nodo.icono}"></i>\n ${nodo.nombre}`
        if (nodo.tipo == "link") {
            menuHTML += `<li><a ${link}>${sCaption}</a></li>\n`
        } else {
            identificadorMenuHijo = `menu_${nodo.id}`
            menuHTML += `<li>
                        <a href="#${identificadorMenuHijo}" data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                            ${sCaption}
                        </a>\n`
            menuHTML += armarSegundo(menuJson, nodo.id, nodo.tipo, identificadorMenuHijo)
            menuHTML += `</li>\n`
        }

    });
    menuHTML += `</ul>`;
    console.log("html----",menuHTML);
    document.getElementById(idContainer).innerHTML = menuHTML;
}

function armarSegundo(menuJson, padreId, TipoPadre, identificadorMenuHijo) {

    console.log("armarSegundo")
    let datos = getHijosOrdenados(menuJson, padreId)
    let str = ""

    str += `<ul class="collapse list-unstyled" id="${identificadorMenuHijo}">`

    datos.forEach(padre => {
        let sTarget = `target="main-iframe"`;
        let sCaption = `<i class="fas fa-${padre.icono} fa-fw me-2"></i>\n ${padre.nombre}`
        if (padre.tipo == "link") {
            str += `<li><a href="${padre.ruta}"  ${sTarget}  class="menu-link">${sCaption}</a></li>\n`
        } else {
            identificadorMenuHijo = `submenu-${padre.id}`
            str += `<li>
                    <a href="#${identificadorMenuHijo}" 
                        data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                        ${sCaption}
                    </a>\n`
            str += armarTercero(menuJson, padre.id, padre.tipo, identificadorMenuHijo)
            str += `</li>\n`
            console.log(str);
        }

    });
    str += `</ul>`
    return str;
}

function armarTercero(menuJson, padreId, TipoPadre, identificadorMenuHijo) {
    console.log("armarTercero")
    let datos = getHijosOrdenados(menuJson, padreId)
    let str = "<li>"
    datos.forEach(padre => {
        console.log("padre", padre);
        let sCaption = `<i class="fas fa-${padre.icono} fa-fw me-2"></i> ${padre.nombre}</a></li>`
        if (padre.tipo == "link") {
            str += `<li><a href="${padre.ruta}" data-bs-toggle="collapse" target="main-iframe" class="menu-link">${sCaption}\n`
        }
        if (padre.tipo == "padre") {
            identificadorMenuHijo = `submenu-${padre.id}`
            str += `<li><a href="#${identificadorMenuHijo}" target="main-iframe" class="menu-link">${sCaption}\n`
            //menuHTML += armarSegundo(menuJson,padre.id, padre.tipo ,identificadorMenuHijo)
            str += `</li>\n`
        }
    });

    return str
}

function getHijosOrdenados(menuJson, padreId) {
    try {
        // Verificamos si menuJson está vacío
        if (menuJson === "") {
            return menuJson;
        } else {
            // Filtramos los elementos que tienen el id_padre igual al padreId y los ordenamos por el campo "orden"
            return menuJson
                .filter(item => item.id_padre === padreId)
                .sort((a, b) => a.orden - b.orden);
        }
    } catch (error) {
        // Capturamos cualquier error y mostramos un mensaje en la consola
        console.error("Error al obtener los hijos ordenados:", error);
        return []; // Devolvemos un arreglo vacío en caso de error
    }
}
console.log("dashboard-token.js cargado (versión con jQuery para UI).");