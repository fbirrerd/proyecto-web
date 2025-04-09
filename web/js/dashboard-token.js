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
        let menusGenerales = tokenData.menusGenerales;
        let menusEspecificos = tokenData.menusEspecificos;
        let empresas = tokenData.empresas;


        LoadEmpresas(empresas)

        alert(menusGenerales);
        console.log("menusGenerales",menusGenerales);        
        LoadMenu(menusGenerales, "leftMenuGeneralContainer")
        // alert(menusEspecificos);
        // console.log("menusEspecificos",menusEspecificos);        
            // LoadMenu(menusEspecificos, "leftMenuEspecificoContainer")

        alert("fin");        

    } else {
        console.log('No token found in localStorage');
    }

    function getHijosOrdenados(menuJson, padreId) {
        if(menuJson==""){
            console.log("1")
            return menuJson;
        }else{
            console.log("2")
            return menuJson
                .filter(item => item.id_padre === padreId)
                .sort((a, b) => a.orden - b.orden);
        }
    }

    function LoadEmpresas(empresasJSON) {
        const dropdownMenu = document.querySelector('.dropdown-menu');
    
        // Limpiar el contenido inicial del dropdown (opcional)
        dropdownMenu.innerHTML = '';
    
        // Verifica si empresasJSON tiene datos
        console.log("Empresas JSON:", empresasJSON);
    
        if (empresasJSON.length > 0) {
            cargarNombreEmpresa(empresasJSON[0].nombre);
        } else {
            console.log("No hay empresas en el JSON.");
        }
    
        empresasJSON.forEach((empresa, index) => {
            const listItem = document.createElement('li');
            const linkItem = document.createElement('a');
            linkItem.classList.add('dropdown-item');
            linkItem.href = '#'; // Puedes agregar aquí la URL específica de cada empresa si la tienes
            linkItem.textContent = empresa.nombre;
            listItem.appendChild(linkItem);
            dropdownMenu.appendChild(listItem);
    
            // Agregar un separador después de cada empresa, excepto la última
            if (index < empresasJSON.length - 1) {
                const divider = document.createElement('li');
                const hr = document.createElement('hr');
                hr.classList.add('dropdown-divider');
                divider.appendChild(hr);
                dropdownMenu.appendChild(divider);
            }
        });
    }
    


    function LoadMenu(menuJson, idContainer) {
        let datos = getHijosOrdenados(menuJson, null);
        let menuHTML = `<ul class="list-unstyled components mb-5">`;
        let strPadre = "";

        console.log("datos",datos)

        datos.forEach(padre => {
            let linkPadre = null;
            let strHijo = "";
            let strNieto = "";
            let strTataraNieto = "";
            let identificadorMenuHijo = "";
            let sTarget = `target="main-iframe"`;
            let sCaption = `<i class="fas fa-${padre.icono} fa-fw me-2"></i>\n ${padre.nombre}`
            console.log("padre.tipo",padre.tipo);
            if (padre.tipo == "url") {
                menuHTML += `<li><a href="${padre.url}" ${sTarget} class="menu-link">${sCaption}</a></li>\n`
            }
            let tipo = "link";
            if(padre.ruta){
                tipo = "padre";
            }
            alert(padre.ruta, tipo)
            if (tipo == "padre") {
                identificadorMenuHijo = `menu-${padre.id}`
                menuHTML += `<li>
                            <a href="#${identificadorMenuHijo}" 
                                data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                                ${sCaption}
                            </a>\n`
                menuHTML += armarSegundo(menuJson, padre.id, padre.tipo, identificadorMenuHijo)
                menuHTML += `</li>\n`
            }

        });
        menuHTML += `</ul>`;
        console.log(menuHTML);
        document.getElementById(idContainer).innerHTML = menuHTML;
    }

    function armarSegundo(menuJson, padreId, TipoPadre, identificadorMenuHijo) {

        let datos = getHijosOrdenados(menuJson, padreId)
        let str = ""
        if (TipoPadre == "menu") {

        }

        str += `<ul class="collapse list-unstyled" id="${identificadorMenuHijo}">`

        datos.forEach(padre => {
            // str += `\n${padre.tipo}\n`
            let sTarget = `target="main-iframe"`;
            let sCaption = `<i class="fas fa-${padre.icono} fa-fw me-2"></i>\n ${padre.nombre}`
            if (padre.tipo == "url") {
                str += `<li><a href="${padre.url}"  ${sTarget}  class="menu-link">${sCaption}</a></li>\n`
            }
            if (padre.tipo == "padre") {
                identificadorMenuHijo = `submenu-${padre.id}`
                str += `<li>
                        <a href="#${identificadorMenuHijo}" 
                            data-bs-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                            ${sCaption}
                        </a>\n`
                str += armarSegundo(menuJson, padre.id, padre.tipo, identificadorMenuHijo)
                str += `</li>\n`
            }

        });
        str += `</ul>`
        return str;
    }

    function armarTercero(menuJson, padreId, TipoPadre, identificadorMenuHijo) {

        let datos = getHijosOrdenados(menuJson, padreId)
        let str = "<li>"
        datos.forEach(padre => {
            let sCaption = `<i class="fas fa-${padre.icono} fa-fw me-2"></i> ${padre.nombre}</a></li>`
            if (padre.tipo == "url") {
                str += `<li><a href="${padre.url}" data-bs-toggle="collapse" target="main-iframe" class="menu-link">${sCaption}\n`
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
})

function cargarNombreEmpresa(empresaNombre){
    $("#companyDropdown").html(`<i class="fas fa-building fa-fw me-1"></i> ${empresaNombre}`);
}


console.log("dashboard-token.js cargado (versión con jQuery para UI).");