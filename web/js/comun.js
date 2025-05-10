
let API_URL = "http://localhost:8200/api/";
let API_URL_VERSION = "v1/";

function showInfo($mensaje) {
  mostrarAlerta({
    mensaje: $mensaje,
    tipo: "success",
    duracion: 10,
  });
}
function showWarning($mensaje) {
  mostrarAlerta({
    mensaje: $mensaje,
    tipo: "warning",
    duracion: 10,
  });
}
function showDanger($mensaje) {
  mostrarAlerta({
    mensaje: $mensaje,
    tipo: "danger",
    duracion: 10,
  });
}

function mostrarAlerta({
  mensaje = "Operación realizada",
  tipo = "success", // success, danger, warning, info
  duracion = 30,
} = {}) {
  let alerta = document.getElementById("alerta");

  // Si no existe, la crea
  if (!alerta) {
    alerta = document.createElement("div");
    alerta.id = "alerta";
    alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
    alerta.role = "alert";
    alerta.style =
      "display:none; position: fixed; top: 10px; right: 10px; z-index: 1050;";

    alerta.innerHTML = `
                <span id="mensaje-alerta">${mensaje}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
            `;

    document.body.appendChild(alerta);
  } else {
    // Reutiliza el contenedor, cambia contenido y clase
    alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
    document.getElementById("mensaje-alerta").textContent = mensaje;
  }

  // Mostrar la alerta
  alerta.style.display = "block";

  // Ocultar después de la duración especificada
  setTimeout(() => {
    alerta.style.display = "none";
  }, duracion * 1000);
}

async function fetchMultiple(endpoints = [], onSuccess = () => {}, onError = () => {}) {
  try {
      const responses = await Promise.all(
          endpoints.map(endpoint => callApi('GET', endpoint))
      );
      onSuccess(responses);
  } catch (err) {
      onError(err);
      showDanger("No se puede conectar con el servidor");
  }
}


function  callApi(method, endpoint, params) {
  // Crear el elemento del mensaje de carga
  // Crear el elemento del icono de carga de Font Awesome
  const loadingIcon = document.createElement("i");
  loadingIcon.classList.add("fas", "fa-spinner", "fa-spin"); // Clases de Font Awesome para el icono de carga
  loadingIcon.style.position = "absolute";
  loadingIcon.style.top = "10px";
  loadingIcon.style.left = "10px";
  loadingIcon.style.fontSize = "30px"; // Ajusta el tamaño del icono según sea necesario
  document.body.appendChild(loadingIcon);

  // Verificar si ya existen credenciales en localStorage
  let auth = getAuthFromLocalStorage();
  let headers = {};
  if (auth) {
    const authHeader = "Basic " + btoa(auth.username + ":" + auth.password);
    headers["Authorization"] = authHeader;
  }

  let $url = `${API_URL}${API_URL_VERSION}${endpoint}`;
  // logToConsole(`Llamando a: ${$url}`, `Metodo: ${method}, parametros: ${JSON.stringify(params)} `);

  // Configuración de la solicitud AJAX
  const config = {
    url: $url,
    method: method,
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify(params),
    headers: headers, // Añadimos los encabezados (incluyendo la autenticación)
    success: function (response) {
      document.body.removeChild(loadingIcon); // Elimina el mensaje de carga

      return response;
    },
    error: function (xhr, status, error) {
      document.body.removeChild(loadingIcon); // Elimina el mensaje de carga

      logToConsole(
        "Error en la solicitud",
        `Error al hacer la solicitud: ${error}`
      );
      return {
        respuesta: false,
        error: `Error al hacer la solicitud: ${error}`,
      };
    },
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
    message: message,
  };
}

/**
 * Obtiene las credenciales de autenticación desde localStorage.
 * @returns {object|null} - Devuelve un objeto con 'username' y 'password' o null si no existen.
 */
function getAuthFromLocalStorage() {
  const auth = localStorage.getItem("auth");
  logToConsole(
    "auth",
    auth
      ? `Existen archivos de autenticacion: ${JSON.parse(auth)}`
      : "Sin datos de autenticacion"
  );
  return auth ? JSON.parse(auth) : null;
}

$(document).on("change", ".icon-select", function () {
  const selectedIcon = $(this).val();
  const id = $(this).attr("id").split("select-icon-")[1];

  // Cambiar el icono en el div de vista previa
  $(`#icon-preview-${id}`).html(
    selectedIcon ? `<i class="${selectedIcon} fa-lg"></i>` : ""
  );

  // Actualizar el hidden input
  $(`#icono-${id}`).val(selectedIcon);
});

function togglePasswordVisibility(passwordSelector, iconSelector) {
  const $passwordInput = $(passwordSelector);
  const $toggleIcon = $(iconSelector);

  // Mostrar ícono si hay texto
  $passwordInput.on("input", function () {
    if ($(this).val().length > 0) {
      $toggleIcon.show();
    } else {
      $toggleIcon.hide();
      $passwordInput.attr("type", "password");
      $toggleIcon.removeClass("fa-eye-slash").addClass("fa-eye");
    }
  });

  // Alternar visibilidad de la contraseña
  $toggleIcon.on("click", function () {
    const type =
      $passwordInput.attr("type") === "password" ? "text" : "password";
    $passwordInput.attr("type", type);
    $(this).toggleClass("fa-eye fa-eye-slash");
  });

  if ($passwordInput.val().length === 0) {
    $toggleIcon.hide();
  }
}

function setToken(token) {
  localStorage.setItem("accessToken", token);
  console.debug("Token guardado en localStorage.");
}

/**
 * Elimina el token JWT de localStorage.
 */
function removeToken() {
  localStorage.removeItem("accessToken");
  console.debug("Token eliminado de localStorage.");
}

console.log("comun.js cargado (versión con jQuery para UI).");
