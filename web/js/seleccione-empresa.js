document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    // Limpia mensajes de error al cargar
    hideMessage('error-message');

    // Si ya está autenticado, redirigir al dashboard
    if (isAuthenticated()) {
        console.log("Usuario ya autenticado, redirigiendo al dashboard.");
        window.location.href = '/dashboard.html'; // Ajusta la ruta si es necesario
        return; // Detiene la ejecución del resto del script
    }


    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita el envío tradicional del formulario
        hideMessage('error-message'); // Oculta errores previos

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');

        // Crea el cuerpo de la petición en formato FormData (como espera OAuth2PasswordRequestForm)
        const formData = new URLSearchParams();
        formData.append('username', usernameInput.value.trim());
        formData.append('password', passwordInput.value); // No quitar espacios a la contraseña

        console.log(`Intentando login para: ${usernameInput.value.trim()}`);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/auth/token`, {
                method: 'POST',
                // No necesitas 'Content-Type': 'application/x-www-form-urlencoded' explícitamente
                // al usar URLSearchParams con fetch, él lo añade.
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                // Intenta obtener un mensaje de error más específico de la API si existe
                const errorDetail = data.detail || `Error ${response.status}: ${response.statusText}`;
                console.error('Error en login:', errorDetail);
                showError(errorDetail, 'error-message');
            } else {
                // Login exitoso
                console.log('Login exitoso:', data);
                if (data.access_token) {
                    setToken(data.access_token); // Guarda el token usando common.js
                    console.log('Redirigiendo al dashboard...');
                    window.location.href = '/dashboard.html'; // Redirige al dashboard
                } else {
                     console.error('Respuesta exitosa pero sin access_token:', data);
                     showError('Respuesta inesperada del servidor.', 'error-message');
                }
            }

        } catch (error) {
            console.error('Fallo en la petición de login:', error);
            // Muestra un error genérico si falla la petición fetch (ej: red)
             showError(`No se pudo conectar con el servidor. ${error.message || ''}`, 'error-message');
        }
    });
});