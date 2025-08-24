$(document).ready(function() {
    const savedUsername = localStorage.getItem("rememberedUsername");
    const savedPassword = localStorage.getItem("rememberedPassword");

    if (savedUsername && savedPassword) {
      document.getElementById("username").value = savedUsername;
      document.getElementById("password").value = savedPassword;
      document.getElementById("rememberMe").checked = true;
    }
    
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
            showWarning("Ingrese un usuario y contraseña válido")
        }

        // Parámetros para la API
        const params = {
            username: username,
            password: password
        };

        const remember = document.getElementById("rememberMe").checked;
            
        if (remember) {
          localStorage.setItem("rememberedUsername", username);
          localStorage.setItem("rememberedPassword", password);
        } else {
          localStorage.removeItem("rememberedUsername");
          localStorage.removeItem("rememberedPassword");
        }


        // Llamada a la API para autenticar al usuario con Basic Auth
        callApi('POST', 'auth/', params)
            .done(function(response) {
                if (response.respuesta) {
                    // Si la respuesta es exitosa y 'cambioClave' es true, muestra un mensaje adecuado
                    if (response.data.cambioClave) {
                        showInfo("Es necesario cambiar tus credenciales");                        
                    } else {
                        updateDataSystem(response.data);

                        localStorage.setItem('paginaInicio',response.data.pagina.inicio);
                        localStorage.setItem('dashboard',response.data.pagina.dashboard);

                        window.location.href = response.data.pagina.dashboard + '.html'; // Redirige a la página para cambiar la clave
                    }
                } else {
                    // Si hay un error en la respuesta
                    showWarning("Existe un error con tus credenciales");                        
                }
            })
            .fail(function() {
                // En caso de que falle la solicitud
                showDanger("No se puede conectar con el servidor");                
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