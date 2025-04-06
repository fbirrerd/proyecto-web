/**
 * Funciones Comunes de JavaScript (con jQuery para utilidades de UI)
 * Asegúrate de que jQuery esté cargado ANTES que este script.
 */

// --- Configuración ---
const API_BASE_URL = 'http://localhost:8200/api/v1'; // URL base de tu API FastAPI (ajusta si es necesario)

// --- Autenticación (Manejo de Token JWT) ---
// (Estas funciones usan localStorage, no necesitan jQuery)

/**
 * Obtiene el token JWT almacenado en localStorage.
 * @returns {string|null} El token o null si no existe.
 */
function getToken() {
    return localStorage.getItem('accessToken');
}

/**
 * Guarda el token JWT en localStorage.
 * @param {string} token - El token JWT a guardar.
 */
function setToken(token) {
    localStorage.setItem('accessToken', token);
    console.debug("Token guardado en localStorage.");
}

/**
 * Elimina el token JWT de localStorage.
 */
function removeToken() {
    localStorage.removeItem('accessToken');
    console.debug("Token eliminado de localStorage.");
}

/**
 * Verifica si hay un token válido almacenado.
 * @returns {boolean} True si hay un token, false si no.
 */
function isAuthenticated() {
    return !!getToken();
}

/**
 * Redirige a la página de login si el usuario no está autenticado.
 */
function redirectToLoginIfUnauthenticated() {
    // La lógica original está comentada, se mantiene igual.
    // if (!isAuthenticated()) {
    //     console.warn("Usuario no autenticado. Redirigiendo a login.");
    //     window.location.href = '/index.html'; // O la ruta correcta a tu login
    // }
}

// --- Utilidades de UI (Adaptadas a jQuery) ---

/**
 * Muestra un mensaje de error en un elemento específico usando jQuery.
 * @param {string} message - El mensaje de error a mostrar.
 * @param {string} elementId - El ID del elemento donde mostrar el mensaje (ej: 'error-message').
 */
function showError(message, elementId = 'error-message') {
    const $errorElement = $('#' + elementId); // Selección con jQuery
    if ($errorElement.length) { // Verifica si el elemento existe
        $errorElement
            .text(message) // Establece el texto
            .removeClass('d-none alert-success') // Quita clases (incluyendo d-none si existe)
            .addClass('alert-danger') // Añade clase de error
            .show(); // Asegura que sea visible (alternativa a quitar d-none)
    } else {
        console.error(`Elemento con ID '${elementId}' no encontrado para mostrar error.`);
        alert(`Error: ${message}`); // Fallback a alert
    }
}

/**
 * Muestra un mensaje de éxito en un elemento específico usando jQuery.
 * @param {string} message - El mensaje de éxito a mostrar.
 * @param {string} elementId - El ID del elemento donde mostrar el mensaje (ej: 'success-message').
 * @param {number} duration - Duración en ms para ocultar el mensaje (0 para no ocultar).
 */
function showSuccess(message, elementId = 'success-message', duration = 5000) {
    const $successElement = $('#' + elementId); // Selección con jQuery
    if ($successElement.length) {
        $successElement
            .text(message)
            .removeClass('d-none alert-danger')
            .addClass('alert-success')
            .show();

        if (duration > 0) {
            // Usa setTimeout para ocultar después de la duración
            setTimeout(() => {
                 // Llama a la versión jQuery de hideMessage o directamente .hide() / .addClass()
                 hideMessage(elementId); // Llama a la función hideMessage adaptada abajo
                 // o directamente: $successElement.addClass('d-none').text('');
            }, duration);
        }
    } else {
        console.error(`Elemento con ID '${elementId}' no encontrado para mostrar éxito.`);
        alert(`Éxito: ${message}`); // Fallback a alert
    }
}

/**
 * Oculta un elemento de mensaje usando jQuery.
 * @param {string} elementId - El ID del elemento a ocultar.
 */
function hideMessage(elementId) {
    const $messageElement = $('#' + elementId); // Selección con jQuery
    if ($messageElement.length) {
         // Oculta añadiendo la clase d-none (estilo Bootstrap) y limpiando texto
        $messageElement.addClass('d-none').text('');
        // Alternativa: usar .hide() de jQuery si no dependes de la clase d-none
        // $messageElement.hide().text('');
    }
}


// --- Formateo y Otras Utilidades ---
// (Estas funciones usan APIs nativas del navegador, no necesitan jQuery)

/**
 * Formatea un objeto Date o un string de fecha ISO a un formato legible.
 * @param {Date|string} dateInput - La fecha a formatear.
 * @param {object} options - Opciones para Intl.DateTimeFormat (ej: { year: 'numeric', month: 'long', day: 'numeric' }).
 * @returns {string} La fecha formateada o un string vacío si la entrada es inválida.
 */
function formatDate(dateInput, options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) {
    try {
        const date = (dateInput instanceof Date) ? dateInput : new Date(dateInput);
        if (isNaN(date.getTime())) {
            return '';
        }
        // Nota: 'es-CL' se basa en la ubicación detectada. Ajusta si es necesario.
        return new Intl.DateTimeFormat('es-CL', options).format(date);
    } catch (error) {
        console.error("Error formateando fecha:", error);
        return '';
    }
}

/**
 * Obtiene la dirección IP pública del cliente usando un servicio externo.
 * @returns {Promise<string|null>} La IP pública o null en caso de error.
 */
async function getPublicIP() {
    // Usa fetch nativo
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        if (!response.ok) {
            throw new Error(`Error ${response.status} al obtener IP`);
        }
        const data = await response.json();
        console.debug("IP Pública obtenida:", data.ip);
        return data.ip;
    } catch (error) {
        console.error("No se pudo obtener la IP pública:", error);
        return null;
    }
}

/**
 * Obtiene la dirección IP "local" que el navegador expone a través de WebRTC.
 * @returns {Promise<string|null>} La IP local (estimada) o null.
 */
async function getLocalIP() {
    // Usa RTCPeerConnection nativo
    console.warn("La función getLocalIP() puede tener implicaciones de privacidad y no ser fiable.");
    return new Promise((resolve) => {
        const pc = new RTCPeerConnection({ iceServers: [] });
        pc.createDataChannel('');
        let foundIP = false; // Flag local

        pc.onicecandidate = (e) => {
            if (!e || !e.candidate || !e.candidate.candidate) {
                if (!foundIP) {
                    console.warn("No se pudo determinar la IP local vía WebRTC (puede estar deshabilitado o bloqueado).");
                    resolve(null);
                }
                return;
            }
            const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
            const match = ipRegex.exec(e.candidate.candidate);
            if (match && match[1] && !foundIP) {
                if (match[1] !== '127.0.0.1' && !match[1].startsWith('::')) {
                    foundIP = true;
                    console.debug("IP Local (estimada vía WebRTC):", match[1]);
                    pc.close();
                    resolve(match[1]);
                }
            }
        };
        pc.createOffer()
          .then(offer => pc.setLocalDescription(offer))
          .catch(err => {
              console.error("Error creando oferta WebRTC:", err);
              resolve(null);
          });
        setTimeout(() => {
            if (!foundIP) {
                console.warn("Timeout esperando IP local vía WebRTC.");
                try { pc.close(); } catch (e) {}
                resolve(null);
            }
        }, 1000);
    });
}

console.log("common.js cargado (versión con jQuery para UI).");