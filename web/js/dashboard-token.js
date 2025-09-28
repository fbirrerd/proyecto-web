$(document).ready(function () {

    function getDatos() {
        let cadena = localStorage.getItem('dataSystem')
        let data = JSON.parse(cadena);
        return data;
    }

    let data = getDatos();
    console.log(data);
    if (data) {
        let token = data.token;
        let empresas = data.empresas;

        localStorage.setItem('empresa_id', data.empresaSeleccionada);
        localStorage.setItem('usuario_id', data.usuario.id);

        LoadEmpresas(empresas)
        IniciarMenu(data);
        iniciarContador(data.duracionAcceso.minutos); 
    } else {
        console.log('No token found in localStorage');

    }

    function obtenerPaginaSinExtension() {
        // Obtenemos la ruta completa de la URL
        let ruta = window.location.pathname; // "/carpeta/pagina.html"

        // Obtenemos solo el nombre del archivo
        let archivo = ruta.substring(ruta.lastIndexOf('/') + 1); // "pagina.html"

        // Quitamos la extensión si existe
        let nombreSinExtension = archivo.split('.')[0]; // "pagina"

        return nombreSinExtension;
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
    LoadMenuModulo(tokenData.modulos, "leftMenuModulosContainer")
}

function LoadMenu(menuJson, idPadre, idContainer) {
    if(menuJson==null){
        return
    }
    let data = getHijosOrdenados(menuJson, idPadre);
    let menuHTML = "";
    let urlInicio = localStorage.getItem('paginaInicio');
    if(data.length!=0){
        menuHTML = `<ul class="list-unstyled components mb-5">`;
        //INICIO
        menuHTML += `
            <li>
                <a onclick="abrirEnIframe('${urlInicio}', this)" 
                   title="Vista principal" 
                   href="#" 
                   target="mainFrame" 
                   class="menu-link">
                   <i class="fas fa-solid fa-dashboard fa-fw me-2"></i> Dashboard
                </a>
            </li>`;        
            data.forEach(nodo => {
            let identificadorMenuHijo = `submenu-${nodo.id}`;
            if(tieneHijos(menuJson,nodo.id)){
                menuHTML += `<li>
                <a href="#${identificadorMenuHijo}" title="${nodo.descripcion || ''}" target="mainFrame" data-bs-toggle="collapse" aria-expanded="false" class="menu-principal">
                <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
                </a>` 
                menuHTML += loadSubMenu(menuJson, nodo.id, identificadorMenuHijo);         
            }else{
                menuHTML += `<li>
                    <a onclick="abrirEnIframe('${nodo.url}',this.id)" title="${nodo.descripcion || ''}"  href="#" target="mainFrame" class="menu-link">
                    <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
                    </a>`
            }
        });
        menuHTML += `</ul>`;
        //console.log("html----", menuHTML);
        
    }
    document.getElementById(idContainer).innerHTML = menuHTML;
}

function loadSubMenu(menuJson, idPadre, identificadorMenuHijo) {

    let data = getHijosOrdenados(menuJson, idPadre);

    // console.log("datos", identificadorMenuHijo, datos);
    let menuHTML = `<ul class="collapse list-unstyled" id="${identificadorMenuHijo}">`


    let strPadre = "";
    data.forEach(nodo => {
        let identificadorMenuHijo = `submenu-${nodo.id}`;

        if(tieneHijos(menuJson,nodo.id)){
            menuHTML += `<li>
            <a href="#${identificadorMenuHijo}" title="${nodo.descripcion || ''}" target="mainFrame" data-bs-toggle="collapse" aria-expanded="false" class="menu-principal">
            <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
            </a>` 
            menuHTML += loadSubMenu(menuJson, nodo.id, identificadorMenuHijo);  
        }else {
            menuHTML += `<li>
                <a onclick="abrirEnIframe('${nodo.url}',this)" title="${nodo.descripcion || ''}" href="#" target="mainFrame" class="menu-link">
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

function LoadMenuModulo(menuJson, idContainer) {
    if(menuJson==null){
        return
    }

    
    let menuHTML = `<ul class="list-unstyled">`;
    menuJson.forEach(nodo => {
        menuHTML += `<li>
                        <a href="#${nodo.nombre}" title="${nodo.descripcion || ''}" target="mainFrame" data-bs-toggle="collapse" aria-expanded="false" class="menu-principal">
                        <i class="fas ${nodo.icono} fa-fw me-2"></i> ${nodo.nombre}
                        </a>`
                        menuHTML += loadSubMenu(nodo.arbol, null, nodo.nombre); 
                    // </li>`
    });
    menuHTML += `</ul>`;
    console.log(menuHTML);
    document.getElementById(idContainer).innerHTML = menuHTML;

}

function abrirEnIframe(url, linkElement) {
    if (!url) {
        console.warn("URL no válida");
        return;
    }

    // Quitar el "/" inicial si existe
    if (url.startsWith("/")) {
        url = url.substring(1);
    }
    const iframeUrl = url.endsWith(".html") ? url : url + ".html";
    console.log("Cargando en iframe:", iframeUrl);
    // Cambiar la URL en el iframe
    $("#mainFrame").attr("src", iframeUrl);
    // Manejar estilos activos
    $("ul li").removeClass("activo");
    $(linkElement).closest("li").addClass("activo");
}

function iniciarContador(minutos) {
    let tiempoRestante;

    // Si ya hay tiempo guardado en sessionStorage, úsalo
    if (localStorage.getItem('tiempoRestante')) {
        tiempoRestante = parseInt(localStorage.getItem('tiempoRestante'));
    } else {
        tiempoRestante = minutos * 60; // convierte a segundos
        localStorage.setItem('tiempoRestante', tiempoRestante);
    }

    const intervalo = setInterval(() => {
        let horas = Math.floor(tiempoRestante / 3600);
        let minutosMostrados = Math.floor((tiempoRestante % 3600) / 60);
        let segundos = tiempoRestante % 60;

        // formatea con ceros a la izquierda
        horas = horas < 10 ? '0' + horas : horas;
        minutosMostrados = minutosMostrados < 10 ? '0' + minutosMostrados : minutosMostrados;
        segundos = segundos < 10 ? '0' + segundos : segundos;

        $('#contador-sesion').text(`${horas}:${minutosMostrados}:${segundos}`);

        if (tiempoRestante <= 0) {
            clearInterval(intervalo);
            cerrarSesion();
        } else {
            tiempoRestante--;
            localStorage.setItem('tiempoRestante', tiempoRestante);
        }
    }, 1000);
}

    // function cerrarSesion() {
    //     localStorage.removeItem("dataSystem"); // Borra el localStorage
    //     localStorage.removeItem("tiempoRestante"); // Borra el localStorage
    //     localStorage.removeItem('empresa_id');
    //     localStorage.removeItem('usuario_id');
    //     localStorage.removeItem('dashboard');
    //     localStorage.removeItem('paginaInicio');
        
    //     window.location.href = 'index.html'; // Redirige a index.html
    // }

console.log("dashboard-token.js cargado (versión con jQuery para UI).");