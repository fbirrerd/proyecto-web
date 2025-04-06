function getToken() {
    return localStorage.getItem('dataSystem');
}
$(document).ready(function() {




    // Verificar el estado del sidebar al cargar la página
    if (localStorage.getItem('sidebarState') === 'hidden') {
        $('#sidebar').addClass('active');
    }

    // Función para alternar el estado del sidebar y guardarlo en localStorage
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');

        // Guardar el estado en localStorage
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
    
    
    // Manejar enlaces del menú para iframe o enlaces externos
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