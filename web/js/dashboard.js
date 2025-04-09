
$(document).ready(function() {

    function getDatos() {
        let cadena = localStorage.getItem('dataSystem')
        let data = JSON.parse(cadena);
        return data;
    }

    $(document).on("click", ".empresa-opcion", function (e) {
        e.preventDefault();
        const empresaId = $(this).data("id");
        const empresaNombre = $(this).text();

        cargarNombreEmpresa(empresaNombre);
        
        let data = getDatos();
        console.log(empresaId);
        const params = {
            "token": data.token,
            "empresaid": empresaId
        };        
        
        // Llamar a la API con la empresa seleccionada
        callApi('POST', 'auth/reload', params)
            .done(function(response) {
                console.log(response.data);
                if (response.respuesta) {
                    localStorage.setItem('dataSystem', JSON.stringify(response.data));
                    IniciarMenu(response.data);

                } else {

                }
            })
            .fail(function() {
                // En caso de que falle la solicitud
                $('#error-message').text('Hubo un error al conectar con el servidor. Intenta de nuevo.').removeClass('d-none');
            });

    });   

    $('#logout-button').on('click', function (e) {
        e.preventDefault(); // Evita el comportamiento predeterminado del enlace
        localStorage.removeItem("dataSystem"); // Borra el localStorage
        window.location.href = 'index.html'; // Redirige a index.html
    });

    // Verificar el estado del sidebar al cargar la página
    if (localStorage.getItem('sidebarState') === 'hidden') {
        $('#sidebar').addClass('active');
    }

    // Función para alternar el estado del sidebar y guardarlo en localStorage
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            localStorage.setItem('sidebarState', 'hidden');
        } else {
            localStorage.setItem('sidebarState', 'visible');
        }
    });

    $('#theme').on('change', function() {
        const theme = $(this).val();
        $('#theme-stylesheet').attr('href', 'css/desktop-style/' + theme + '.css');
    });
    
    $('#sidebar .menu-link').on('click', function (event) {
        const target = $(this).attr('target');
        const href = $(this).attr('href');

        if (target === '_blank') {
            window.open(href, '_blank');
        } else if (target === 'main-iframe') {
            $('#main-iframe').attr('src', href);
            if ($('#sidebar').hasClass('active')) {
                $('#sidebar').removeClass('active');
            }
        } else {
            window.location.href = href;
        }
        event.preventDefault();
    });

    // Verificar el modo iframe-only
    function checkIframeOnly() {
        const urlParams = new URLSearchParams(window.location.search);
        const iframeOnlyParam = urlParams.get('iframeOnly');

        if (iframeOnlyParam === 'true') {
            $('.wrapper, .navbar-custom, #sidebar, .iframe-container').addClass('iframe-only');
            $('body').css('flex-direction', 'column');
        } else {
            $('.wrapper, .navbar-custom, #sidebar, .iframe-container').removeClass('iframe-only');
            $('body').css('flex-direction', 'flex');
        }
    }
    checkIframeOnly();

});

console.log("dashboard.js cargado (versión con jQuery para UI).");
