// js/login.js

$(document).ready(function() {
    // Cuando el formulario se envíe
    $('#change-password-form').submit(function(event) {
        event.preventDefault();  // Evita el comportamiento predeterminado del formulario (recarga de página)

        // Obtiene los valores de los campos de usuario y contraseña
        const username = $('#username').val();
        const email = $('#email').val();
        const pass1 = $('#new_password').val();
        const pass2 = $('#confirm_new_password').val();

        // Muestra un mensaje de error si no se llenan los campos
        if (!username || !pass1) {
            $('#api-error').text('Por favor, ingresa tu usuario y contraseña.').removeClass('d-none');
            return;
        }

        // Valida si las contraseñas coinciden
        if (pass1 !== pass2) {
            $('#api-error').text('Las contraseñas no coinciden.').removeClass('d-none');
            return;
        }

        // Parámetros para la API
        const params = {
            username: username,
            email: email,
            password: pass1
        };

        // Llamada a la API para autenticar al usuario con Basic Auth
        callApi('PUT', 'auth/', params)
            .done(function(response) {
                if (response.respuesta) {
                    // Si la respuesta es exitosa y 'cambioClave' es true, muestra un mensaje adecuado
                    if (response.data.cambioClave) {
                        $('#error-message').text('Es necesario cambiar tu contraseña.').removeClass('d-none');
                        // Esperamos 5 segundos antes de redirigir a la página de cambio de contraseña
                        setTimeout(function() {
                            window.location.href = 'cambiar_clave.html'; // Redirige a la página para cambiar la clave
                        }, 5000);  // 5 segundos de retraso                        
                    } else {
                        // Esperamos 5 segundos antes de redirigir a la página de cambio de contraseña
                        setTimeout(function() {
                            window.location.href = 'dashboard.html'; // Redirige a la página para cambiar la clave
                        }, 5000);  // 5 segundos de retraso
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
});


function showMessage(message, type) {
    // Limpiar las clases previas (en caso de que ya haya un mensaje mostrado)
    $('#error-message').removeClass('message-error message-warning message-info');
    
    // Establecer el mensaje
    $('#error-message').text(message).removeClass('d-none');
    
    // Agregar la clase correspondiente según el tipo
    switch (type) {
        case 'error':
            $('#error-message').addClass('message-error');
            break;
        case 'warning':
            $('#error-message').addClass('message-warning');
            break;
        case 'info':
            $('#error-message').addClass('message-info');
            break;
        default:
            $('#error-message').addClass('message-info'); // Default to 'info' if no type is provided
    }

    // Ocultar el mensaje después de 5 segundos
    setTimeout(function() {
        $('#error-message').addClass('d-none');
    }, 5000); // El mensaje se ocultará después de 5 segundos
}

console.log("cambiar_clave.js cargado (versión con jQuery para UI).");