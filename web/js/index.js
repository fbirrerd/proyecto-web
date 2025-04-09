$(document).ready(function() {
    $('#togglePassword').on('click', function () {
        const passwordField = $('#password');
        const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
        passwordField.attr('type', type);
        $(this).toggleClass('fa-eye fa-eye-slash');
    });
    $('#btnCambiarClave').click(function(event) {
        window.location.href = 'cambiar_clave.html'; // Redirige a la página para cambiar la clave
    });    

    $('#login-form').submit(function(event) {
        event.preventDefault();  // Evita el comportamiento predeterminado del formulario (recarga de página)

        // Obtiene los valores de los campos de usuario y contraseña
        const username = $('#username').val();
        const password = $('#password').val();

        // Muestra un mensaje de error si no se llenan los campos
        if (!username || !password) {
            $('#error-message').text('Por favor, ingresa tu usuario y contraseña.').removeClass('d-none');
            return;
        }

        // Parámetros para la API
        const params = {
            username: username,
            password: password
        };

        // Llamada a la API para autenticar al usuario con Basic Auth
        callApi('POST', 'auth/', params)
            .done(function(response) {
                if (response.respuesta) {
                    // Si la respuesta es exitosa y 'cambioClave' es true, muestra un mensaje adecuado
                    if (response.data.cambioClave) {
                        $('#error-message').text('Es necesario cambiar tu contraseña.').removeClass('d-none');
                    } else {
                        updateDataSystem(response.data);
                        window.location.href = 'dashboard.html'; // Redirige a la página para cambiar la clave
                    }
                } else {
                    // Si hay un error en la respuesta
                    console.log(response.error);
                    $('#error-message').text(`Error en el login. Verifica tus credenciales. (${response.data.error})`).removeClass('d-none');
                }
            })
            .fail(function() {
                // En caso de que falle la solicitud
                $('#error-message').text('Hubo un error al conectar con el servidor. Intenta de nuevo.').removeClass('d-none');
            });
    });

    function updateDataSystem(newToken) {
        // Verifica si ya existe el token en localStorage
        if (localStorage.getItem('dataSystem')) {
            // Elimina el token existente
            localStorage.removeItem('dataSystem');
        }
        localStorage.setItem('dataSystem', JSON.stringify(newToken));
    }    
});

console.log("login.js cargado (versión con jQuery para UI).");