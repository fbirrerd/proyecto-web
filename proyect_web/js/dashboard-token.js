$(document).ready(function () {

    function getDatos() {
        let cadena = localStorage.getItem('dataSystem')
        let data = JSON.parse(cadena);
        return data;
    }

    let data = getDatos();
    if (data) {
        let token = data.token;
        let empresas = data.empresas;

        LoadEmpresas(empresas)
        IniciarMenu(data);

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

function cargarNombreEmpresa(empresaNombre) {
    $("#companyDropdown").html(`<i class="fas fa-building fa-fw me-1"></i> ${empresaNombre}`);
}

function IniciarMenu(tokenData) {
    LoadMenu(tokenData.menus, null, "leftMenuContainer")
    //LoadMenu(tokenData.menusEspecificos, "leftMenuEspecificoContainer")
}

function LoadMenu(menuJson, idPadre, idContainer) {
    if(menuJson==null){
        return
    }
    let datos = getHijosOrdenados(menuJson, idPadre);
    console.log(datos);
    let menuHTML = `<ul class="list-unstyled components mb-5">`;
    datos.forEach(nodo => {
        let identificadorMenuHijo = `submenu-${nodo.id}`;
        if(tieneHijos(menuJson,nodo.id)){
            menuHTML += `<li>
            <a href="#${identificadorMenuHijo}" title="${nodo.descripcion || ''}" target="main-iframe" data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
            <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
            </a>` 
            menuHTML += loadSubMenu(menuJson, nodo.id, identificadorMenuHijo);         
        }else{
            menuHTML += `<li>
                <a onclick="abrirEnIframe('${nodo.url}',this.id)" title="${nodo.descripcion || ''}"  href="#" target="main-iframe" class="menu-link">
                <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
                </a>`
        }
    });
    menuHTML += `</ul>`;
    //console.log("html----", menuHTML);
    document.getElementById(idContainer).innerHTML = menuHTML;
}

function loadSubMenu(menuJson, idPadre, identificadorMenuHijo) {

    let datos = getHijosOrdenados(menuJson, idPadre);

    console.log("datos", identificadorMenuHijo, datos);
    let menuHTML = `<ul class="collapse list-unstyled" id="${identificadorMenuHijo}">`


    let strPadre = "";
    datos.forEach(nodo => {
        let identificadorMenuHijo = `submenu-${nodo.id}`;

        if(tieneHijos(menuJson,nodo.id)){
            menuHTML += `<li>
            <a href="#${identificadorMenuHijo}" title="${nodo.descripcion || ''}" target="main-iframe" data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
            <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
            </a>` 
            menuHTML += loadSubMenu(menuJson, nodo.id, identificadorMenuHijo);  
        }else {
            menuHTML += `<li>
                <a onclick="abrirEnIframe('${nodo.url}',this)" title="${nodo.descripcion || ''}" href="#" target="main-iframe" class="menu-link">
                <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
                </a>`
        }
    });
    menuHTML += `</ul>`;

    return menuHTML;
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
        console.error("Error al obtener los hijos ordenados:", error);
        return []; // Devolvemos un arreglo vacío en caso de error
    }
}


function tieneHijos(menuJson, padreId) {
    try { 
        return menuJson.filter(item => item.id_padre === padreId).length > 0;
    } catch (error) {
        return false; // Devolvemos un arreglo vacío en caso de error
    }
}

function abrirEnIframe(url, linkElement) {
    url = url?.startsWith("/") ? url.substring(1) : url;
    const $url = url + ".html";
    console.log($url);
    $("#mainFrame").attr("src", $url);

    // Opcional: manejar estilos activos con jQuery
    $("ul li").removeClass("activo");
    $(linkElement).parent().addClass("activo");
}

console.log("dashboard-token.js cargado (versión con jQuery para UI).");