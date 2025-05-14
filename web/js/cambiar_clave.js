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
                        showWarning("Es necesario cambiar tu contraseña.")
                    } else {
                        showInfo("Se ha cambiado correctamente la clave")
                    }
                } else {
                    showWarning("Error en el login")
                }
            })
            .fail(function() {
                showDanger("No se puede conectar con el servidor"); 
            });
    });
});

console.log("cambiar_clave.js cargado (versión con jQuery para UI).");