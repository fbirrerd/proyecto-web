document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificar autenticación al cargar la página
    // Si esta página se carga FUERA del iframe del dashboard, necesita esta verificación.
    // Si siempre se carga DENTRO del iframe, el dashboard ya hizo la verificación.
    // Por seguridad, es bueno tenerla aquí también.
    redirectToLoginIfUnauthenticated();

    const changePasswordForm = document.getElementById('change-password-form');
    const messageArea = document.getElementById('message-area'); // Div para mostrar mensajes

    changePasswordForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        messageArea.innerHTML = ''; // Limpiar mensajes anteriores

        const currentPassword = document.getElementById('current_password').value;
        const newPassword = document.getElementById('new_password').value;
        const confirmNewPassword = document.getElementById('confirm_new_password').value;

        // Validación simple de cliente
        if (newPassword.length < 6) {
            showError('La nueva contraseña debe tener al menos 6 caracteres.', 'message-area');
            return;
        }
        if (newPassword !== confirmNewPassword) {
            showError('Las nuevas contraseñas no coinciden.', 'message-area');
            return;
        }
        if (currentPassword === newPassword) {
             showError('La nueva contraseña no puede ser igual a la actual.', 'message-area');
            return;
        }

        const passwordData = {
            current_password: currentPassword,
            new_password: newPassword,
        };

        console.log("Intentando cambiar contraseña...");

        try {
            const response = await fetchWithAuth('/api/v1/auth/users/change-password', {
                method: 'POST',
                body: JSON.stringify(passwordData), // Enviar como JSON
                // fetchWithAuth añadirá Content-Type y Authorization
            });

             // Un 204 No Content no tiene cuerpo JSON, así que no intentes parsearlo
             if (response.status === 204) {
                 console.log("Contraseña cambiada exitosamente.");
                 showSuccess('Contraseña cambiada exitosamente. Serás redirigido.', 'message-area', 0); // No ocultar automáticamente
                 // Opcional: Redirigir después de un tiempo o al dashboard
                 setTimeout(() => {
                     // Si está en iframe, podría intentar recargar el dashboard padre
                     if (window.parent && window.parent !== window) {
                         // Intenta navegar el iframe a una página de dashboard inicial
                          window.parent.document.getElementById('main-iframe').src = '/iframes/dashboard_content.html';
                     } else {
                         // Si es página independiente, ir al dashboard
                         window.location.href = '/dashboard.html';
                     }
                 }, 3000); // Espera 3 segundos antes de redirigir
                 changePasswordForm.reset(); // Limpia el formulario
            } else {
                 // Si no es 204, intentar leer el cuerpo del error
                 const errorData = await response.json();
                 const errorMessage = errorData.detail || `Error ${response.status}: ${response.statusText}`;
                 console.error('Error al cambiar contraseña:', errorMessage);
                 showError(errorMessage, 'message-area');
            }

        } catch (error) {
            console.error('Fallo en la petición de cambio de contraseña:', error);
            // No mostrar error si fue 'Unauthorized' y ya se redirigió
            if (error.message !== 'Unauthorized') {
                 showError(`Error de conexión o del servidor: ${error.message || ''}`, 'message-area');
            }
        }
    });
});

// Reutilizar funciones de common.js para mostrar mensajes
function showError(message, elementId) {
    const msgDiv = document.getElementById(elementId);
    if (msgDiv) {
        msgDiv.innerHTML = `<div class="alert alert-danger" role="alert">${message}</div>`;
    }
}

function showSuccess(message, elementId) {
     const msgDiv = document.getElementById(elementId);
    if (msgDiv) {
        msgDiv.innerHTML = `<div class="alert alert-success" role="alert">${message}</div>`;
    }
}