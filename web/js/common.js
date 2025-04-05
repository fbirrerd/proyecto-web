/**
 * Funciones Comunes de JavaScript
 */

// --- Configuración ---
const API_BASE_URL = 'http://localhost:8000'; // URL base de tu API FastAPI (ajusta si es necesario)

// --- Autenticación (Manejo de Token JWT) ---

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
    if (!isAuthenticated()) {
        console.warn("Usuario no autenticado. Redirigiendo a login.");
        // Asegúrate de que la ruta a index.html sea correcta desde donde llames esta función
        window.location.href = '/index.html'; // O la ruta correcta a tu login
    }
}

/**
 * Realiza una petición fetch a la API añadiendo automáticamente
 * el header de autorización con el token JWT.
 * @param {string} url - La URL del endpoint de la API (relativa a API_BASE_URL).
 * @param {object} options - Opciones para la función fetch (method, headers, body, etc.).
 * @returns {Promise<Response>} La promesa de la respuesta fetch.
 */
async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    const headers = new Headers(options.headers || {});

    if (token) {
        headers.append('Authorization', `Bearer ${token}`);
    } else {
        console.warn(`Intentando hacer fetch a ${url} sin token.`);
        // Considera si deberías redirigir a login aquí o dejar que el endpoint falle
    }

     // Asegúrate de que Content-Type esté presente para POST/PUT con JSON
    if (options.body && typeof options.body === 'string' && !headers.has('Content-Type')) {
         try {
            JSON.parse(options.body); // Verifica si es JSON válido
            headers.append('Content-Type', 'application/json');
         } catch (e) {
            // No es JSON, no añadir header o manejar otros tipos
            console.debug("El cuerpo de la petición no es JSON, no se añade Content-Type: application/json");
         }
    }


    const fetchOptions = {
        ...options,
        headers: headers,
    };

    const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`;
    console.debug(`Workspace ${fetchOptions.method || 'GET'} a ${fullUrl}`);

    try {
        const response = await fetch(fullUrl, fetchOptions);

        // Si la respuesta es 401 (Unauthorized), puede que el token haya expirado.
        if (response.status === 401) {
            console.warn('Respuesta 401 (Unauthorized) recibida. Posible token expirado.');
            removeToken(); // Limpia el token inválido
            redirectToLoginIfUnauthenticated(); // Redirige a login
            // Lanza un error para detener el flujo actual que esperaba una respuesta válida
            throw new Error('Unauthorized');
        }

        return response;
    } catch (error) {
        console.error(`Error en fetch a ${fullUrl}:`, error);
        // Si el error fue 'Unauthorized' lanzado arriba, relánzalo
        if (error.message === 'Unauthorized') {
            throw error;
        }
        // Lanza un error genérico para otros problemas de red/fetch
        throw new Error(`Error de red o conexión al intentar acceder a ${fullUrl}`);
    }
}


// --- Utilidades de UI ---

/**
 * Muestra un mensaje de error en un elemento específico.
 * @param {string} message - El mensaje de error a mostrar.
 * @param {string} elementId - El ID del elemento donde mostrar el mensaje (ej: 'error-message').
 */
function showError(message, elementId = 'error-message') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('d-none'); // Muestra el elemento (asumiendo Bootstrap)
        errorElement.classList.remove('alert-success');
        errorElement.classList.add('alert-danger');
    } else {
        console.error(`Elemento con ID '${elementId}' no encontrado para mostrar error.`);
        alert(`Error: ${message}`); // Fallback a alert
    }
}

/**
 * Muestra un mensaje de éxito en un elemento específico.
 * @param {string} message - El mensaje de éxito a mostrar.
 * @param {string} elementId - El ID del elemento donde mostrar el mensaje (ej: 'success-message').
 * @param {number} duration - Duración en ms para ocultar el mensaje (0 para no ocultar).
 */
function showSuccess(message, elementId = 'success-message', duration = 5000) {
    const successElement = document.getElementById(elementId);
    if (successElement) {
        successElement.textContent = message;
        successElement.classList.remove('d-none');
        successElement.classList.remove('alert-danger');
        successElement.classList.add('alert-success');
        if (duration > 0) {
            setTimeout(() => hideMessage(elementId), duration);
        }
    } else {
        console.error(`Elemento con ID '${elementId}' no encontrado para mostrar éxito.`);
        alert(`Éxito: ${message}`); // Fallback a alert
    }
}

/**
 * Oculta un elemento de mensaje.
 * @param {string} elementId - El ID del elemento a ocultar.
 */
function hideMessage(elementId) {
     const messageElement = document.getElementById(elementId);
    if (messageElement) {
        messageElement.classList.add('d-none');
        messageElement.textContent = ''; // Limpia el contenido
    }
}


// --- Formateo y Otras Utilidades ---

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
            return ''; // Devuelve vacío si la fecha no es válida
        }
        return new Intl.DateTimeFormat('es-CL', options).format(date); // Ajusta 'es-CL' a tu locale
    } catch (error) {
        console.error("Error formateando fecha:", error);
        return '';
    }
}

/**
 * Obtiene la dirección IP pública del cliente usando un servicio externo.
 * ¡Precaución! Esto depende de un servicio de terceros y puede no ser fiable
 * o tener limitaciones de uso. NO es la IP local del usuario.
 * @returns {Promise<string|null>} La IP pública o null en caso de error.
 */
async function getPublicIP() {
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
 * NOTA: Esto puede no funcionar en todos los navegadores o configuraciones
 * y requiere permiso del usuario. Puede exponer la IP real incluso detrás de VPNs.
 * Úsalo con precaución y considera la privacidad.
 * @returns {Promise<string|null>} La IP local (estimada) o null.
 */
async function getLocalIP() {
     console.warn("La función getLocalIP() puede tener implicaciones de privacidad y no ser fiable.");
     return new Promise((resolve) => {
        // Crea una conexión RTCPeerConnection temporal
        const pc = new RTCPeerConnection({ iceServers: [] });
        pc.createDataChannel(''); // Canal de datos dummy

        // Escucha candidatos ICE (que pueden contener IPs)
        pc.onicecandidate = (e) => {
            if (!e || !e.candidate || !e.candidate.candidate) {
                // Si no hay más candidatos o el evento es nulo, termina
                 if(!pc.__foundIP) { // Si no encontró nada aún
                    console.warn("No se pudo determinar la IP local vía WebRTC (puede estar deshabilitado o bloqueado).");
                    resolve(null);
                 }
                return;
            }

            // Busca direcciones IPv4 en la descripción del candidato
            const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
            const match = ipRegex.exec(e.candidate.candidate);

            if (match && match[1] && !pc.__foundIP) {
                 // Filtra direcciones no útiles (ej: localhost)
                 if (match[1] !== '127.0.0.1' && !match[1].startsWith('::') /* filtra IPv6 por simplicidad */) {
                    pc.__foundIP = true; // Marca que ya encontramos una IP
                    console.debug("IP Local (estimada vía WebRTC):", match[1]);
                    pc.close(); // Cierra la conexión
                    resolve(match[1]);
                 }
            }
        };

        // Inicia la negociación para generar candidatos
        pc.createOffer()
            .then(offer => pc.setLocalDescription(offer))
            .catch(err => {
                 console.error("Error creando oferta WebRTC:", err);
                 resolve(null);
            });

         // Timeout por si no se resuelve nunca
         setTimeout(() => {
             if (!pc.__foundIP) {
                  console.warn("Timeout esperando IP local vía WebRTC.");
                  pc.close();
                  resolve(null);
             }
         }, 1000); // Espera máximo 1 segundo
     });
}


console.log("common.js cargado.");
// Puedes llamar a getLocalIP() aquí si quieres intentar obtenerla al cargar,
// pero es mejor llamarla cuando la necesites.
// getLocalIP().then(ip => console.log("IP Local al cargar:", ip));