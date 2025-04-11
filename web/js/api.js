// js/api.js


let API_URL = 'http://localhost:8200/api/';
let API_URL_VERSION = 'v1/';

/**
 * Función para realizar la solicitud a la API.
 * @param {string} endpoint - El endpoint de la API.
 * @param {string} method - El método HTTP (GET, POST, PUT, DELETE).
 * @param {object} params - Los parámetros para la solicitud.
 * @param {object} auth - Las credenciales para Basic Auth (opcional).
 * @returns {Promise} - Retorna la promesa con la respuesta de la API.
 */
function callApi(method, endpoint, params) {
     // Crear el elemento del mensaje de carga
    // Crear el elemento del icono de carga de Font Awesome
    const loadingIcon = document.createElement('i');
    loadingIcon.classList.add('fas', 'fa-spinner', 'fa-spin'); // Clases de Font Awesome para el icono de carga
    loadingIcon.style.position = 'absolute';
    loadingIcon.style.top = '10px';
    loadingIcon.style.left = '10px';
    loadingIcon.style.fontSize = '30px'; // Ajusta el tamaño del icono según sea necesario
    document.body.appendChild(loadingIcon);


    // Verificar si ya existen credenciales en localStorage
    let auth = getAuthFromLocalStorage();
    let headers = {};
    if (auth) {
        const authHeader = 'Basic ' + btoa(auth.username + ':' + auth.password);
        headers['Authorization'] = authHeader;
    }

    let $url = `${API_URL}${API_URL_VERSION}${endpoint}`
    // logToConsole(`Llamando a: ${$url}`, `Metodo: ${method}, parametros: ${JSON.stringify(params)} `);

    // Configuración de la solicitud AJAX
    const config = {
        url: $url,
        method: method,
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(params),
        headers: headers,  // Añadimos los encabezados (incluyendo la autenticación)
        success: function(response) {
            document.body.removeChild(loadingIcon); // Elimina el mensaje de carga
            
            return response;
        },
        error: function(xhr, status, error) {
            document.body.removeChild(loadingIcon); // Elimina el mensaje de carga
            
            logToConsole('Error en la solicitud', `Error al hacer la solicitud: ${error}`);
            return { respuesta: false, error: `Error al hacer la solicitud: ${error}` };
        }
    };
    let $resultado = $.ajax(config);
    return $resultado;
}

/**
 * Función para imprimir logs en la consola.
 * @param {string} title - Título del log.
 * @param {string|object} message - El mensaje o la respuesta a imprimir.
 */
function logToConsole(title, message) {
    const log = {
        timestamp: new Date().toISOString(),
        title: title,
        message: message
    };
    // console.log(log);
}

/**
 * Obtiene las credenciales de autenticación desde localStorage.
 * @returns {object|null} - Devuelve un objeto con 'username' y 'password' o null si no existen.
 */
function getAuthFromLocalStorage() {
    const auth = localStorage.getItem('auth');
    logToConsole('auth',auth ? `Existen archivos de autenticacion: ${JSON.parse(auth)}`  : 'Sin datos de autenticacion'  )
    return auth ? JSON.parse(auth) : null;
}

console.log("api.js cargado (versión con jQuery para UI).");