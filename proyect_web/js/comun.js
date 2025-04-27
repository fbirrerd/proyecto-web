
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

let iconosFontAwesome = [
  {
    icon: "fa-solid fa-house fa-fw",
    name: "house",
  },
  {
    icon: "fa-solid fa-magnifying-glass fa-fw",
    name: "magnifying-glass",
  },
  {
    icon: "fa-solid fa-user fa-fw",
    name: "user",
  },

  {
    icon: "fa-brands fa-facebook fa-fw",
    name: "facebook",
  },
  {
    icon: "fa-solid fa-check fa-fw",
    name: "check",
  },
  {
    icon: "fa-solid fa-download fa-fw",
    name: "download",
  },
  {
    icon: "fa-brands fa-twitter fa-fw",
    name: "twitter",
  },
  {
    icon: "fa-solid fa-image fa-fw",
    name: "image",
  },
  {
    icon: "fa-solid fa-phone fa-fw",
    name: "phone",
  },
  {
    icon: "fa-solid fa-bars fa-fw",
    name: "bars",
  },
  {
    icon: "fa-solid fa-envelope fa-fw",
    name: "envelope",
  },
  {
    icon: "fa-brands fa-linkedin fa-fw",
    name: "linkedin",
  },
  {
    icon: "fa-solid fa-star fa-fw",
    name: "star",
  },
  {
    icon: "fa-solid fa-location-dot fa-fw",
    name: "location-dot",
  },
  {
    icon: "fa-brands fa-github fa-fw",
    name: "github",
  },
  {
    icon: "fa-solid fa-music fa-fw",
    name: "music",
  },
  {
    icon: "fa-solid fa-wand-magic-sparkles fa-fw",
    name: "wand-magic-sparkles",
  },
  {
    icon: "fa-solid fa-heart fa-fw",
    name: "heart",
  },
  {
    icon: "fa-solid fa-arrow-right fa-fw",
    name: "arrow-right",
  },
  {
    icon: "fa-brands fa-discord fa-fw",
    name: "discord",
  },


  {
    icon: "fa-solid fa-bomb fa-fw",
    name: "bomb",
  },
  {
    icon: "fa-solid fa-poo fa-fw",
    name: "poo",
  },
  {
    icon: "fa-solid fa-camera-retro fa-fw",
    name: "camera-retro",
  },
  {
    icon: "fa-solid fa-xmark fa-fw",
    name: "xmark",
  },
  {
    icon: "fa-brands fa-youtube fa-fw",
    name: "youtube",
  },
  {
    icon: "fa-solid fa-cloud fa-fw",
    name: "cloud",
  },
  {
    icon: "fa-solid fa-comment fa-fw",
    name: "comment",
  },

  {
    icon: "fa-solid fa-caret-up fa-fw",
    name: "caret-up",
  },
  {
    icon: "fa-solid fa-truck-fast fa-fw",
    name: "truck-fast",
  },
  {
    icon: "fa-brands fa-wordpress fa-fw",
    name: "wordpress",
  },
  {
    icon: "fa-solid fa-pen-nib fa-fw",
    name: "pen-nib",
  },
  {
    icon: "fa-solid fa-arrow-up fa-fw",
    name: "arrow-up",
  },
  {
    icon: "fa-solid fa-hippo fa-fw",
    name: "hippo",
  },
  {
    icon: "fa-solid fa-face-smile fa-fw",
    name: "face-smile",
  },

  {
    icon: "fa-solid fa-calendar-days fa-fw",
    name: "calendar-days",
  },

  {
    icon: "fa-solid fa-paperclip fa-fw",
    name: "paperclip",
  },
  {
    icon: "fa-brands fa-slack fa-fw",
    name: "slack",
  },
  {
    icon: "fa-solid fa-shield-halved fa-fw",
    name: "shield-halved",
  },
  {
    icon: "fa-brands fa-figma fa-fw",
    name: "figma",
  },
  {
    icon: "fa-solid fa-file fa-fw",
    name: "file",
  },

  {
    icon: "fa-solid fa-bell fa-fw",
    name: "bell",
  },

  {
    icon: "fa-solid fa-cart-shopping fa-fw",
    name: "cart-shopping",
  },
  {
    icon: "fa-solid fa-clipboard fa-fw",
    name: "clipboard",
  },

  {
    icon: "fa-solid fa-filter fa-fw",
    name: "filter",
  },
  {
    icon: "fa-solid fa-circle-info fa-fw",
    name: "circle-info",
  },
  {
    icon: "fa-solid fa-arrow-up-from-bracket fa-fw",
    name: "arrow-up-from-bracket",
  },
  {
    icon: "fa-solid fa-bolt fa-fw",
    name: "bolt",
  },
  {
    icon: "fa-solid fa-car fa-fw",
    name: "car",
  },
  {
    icon: "fa-solid fa-ghost fa-fw",
    name: "ghost",
  },
  {
    icon: "fa-brands fa-apple fa-fw",
    name: "apple",
  },
  {
    icon: "fa-solid fa-mug-hot fa-fw",
    name: "mug-hot",
  },
  {
    icon: "fa-solid fa-circle-user fa-fw",
    name: "circle-user",
  },

  {
    icon: "fa-solid fa-pen fa-fw",
    name: "pen",
  },
  {
    icon: "fa-brands fa-google fa-fw",
    name: "google",
  },
  {
    icon: "fa-solid fa-umbrella fa-fw",
    name: "umbrella",
  },
  {
    icon: "fa-solid fa-gift fa-fw",
    name: "gift",
  },
  {
    icon: "fa-solid fa-film fa-fw",
    name: "film",
  },
  {
    icon: "fa-brands fa-stripe fa-fw",
    name: "stripe",
  },
  {
    icon: "fa-solid fa-list fa-fw",
    name: "list",
  },
  {
    icon: "fa-solid fa-gear fa-fw",
    name: "gear",
  },
  {
    icon: "fa-brands fa-algolia fa-fw",
    name: "algolia",
  },
  {
    icon: "fa-solid fa-trash fa-fw",
    name: "trash",
  },

  {
    icon: "fa-brands fa-docker fa-fw",
    name: "docker",
  },
  {
    icon: "fa-solid fa-circle-down fa-fw",
    name: "circle-down",
  },

  {
    icon: "fa-solid fa-inbox fa-fw",
    name: "inbox",
  },
  {
    icon: "fa-solid fa-rotate-right fa-fw",
    name: "rotate-right",
  },
  {
    icon: "fa-solid fa-lock fa-fw",
    name: "lock",
  },
  {
    icon: "fa-brands fa-windows fa-fw",
    name: "windows",
  },
  {
    icon: "fa-solid fa-headphones fa-fw",
    name: "headphones",
  },
  {
    icon: "fa-solid fa-barcode fa-fw",
    name: "barcode",
  },
  {
    icon: "fa-solid fa-tag fa-fw",
    name: "tag",
  },
  {
    icon: "fa-solid fa-book fa-fw",
    name: "book",
  },
  {
    icon: "fa-solid fa-bookmark fa-fw",
    name: "bookmark",
  },
  {
    icon: "fa-solid fa-print fa-fw",
    name: "print",
  },
  {
    icon: "fa-solid fa-camera fa-fw",
    name: "camera",
  },

  {
    icon: "fa-solid fa-font fa-fw",
    name: "font",
  },
  {
    icon: "fa-solid fa-video fa-fw",
    name: "video",
  },
  {
    icon: "fa-solid fa-circle-half-stroke fa-fw",
    name: "circle-half-stroke",
  },
  {
    icon: "fa-solid fa-droplet fa-fw",
    name: "droplet",
  },
  {
    icon: "fa-solid fa-pen-to-square fa-fw",
    name: "pen-to-square",
  },

  {
    icon: "fa-solid fa-share-from-square fa-fw",
    name: "share-from-square",
  },

  {
    icon: "fa-solid fa-plus fa-fw",
    name: "plus",
  },
  {
    icon: "fa-solid fa-minus fa-fw",
    name: "minus",
  },
  {
    icon: "fa-brands fa-kickstarter fa-fw",
    name: "kickstarter",
  },
  {
    icon: "fa-solid fa-share fa-fw",
    name: "share",
  },
  {
    icon: "fa-solid fa-circle-exclamation fa-fw",
    name: "circle-exclamation",
  },
  {
    icon: "fa-solid fa-fire fa-fw",
    name: "fire",
  },
  {
    icon: "fa-solid fa-eye fa-fw",
    name: "eye",
  },

  {
    icon: "fa-solid fa-eye-slash fa-fw",
    name: "eye-slash",
  },

  {
    icon: "fa-brands fa-dribbble fa-fw",
    name: "dribbble",
  },
  {
    icon: "fa-solid fa-plane fa-fw",
    name: "plane",
  },
  {
    icon: "fa-solid fa-magnet fa-fw",
    name: "magnet",
  },
  {
    icon: "fa-solid fa-folder fa-fw",
    name: "folder",
  },

  {
    icon: "fa-solid fa-folder-open fa-fw",
    name: "folder-open",
  },

  {
    icon: "fa-solid fa-money-bill fa-fw",
    name: "money-bill",
  },
  {
    icon: "fa-brands fa-dropbox fa-fw",
    name: "dropbox",
  },
  {
    icon: "fa-solid fa-thumbs-up fa-fw",
    name: "thumbs-up",
  },

  {
    icon: "fa-solid fa-thumbs-down fa-fw",
    name: "thumbs-down",
  },

  {
    icon: "fa-solid fa-comments fa-fw",
    name: "comments",
  },

  {
    icon: "fa-solid fa-lemon fa-fw",
    name: "lemon",
  },

  {
    icon: "fa-solid fa-key fa-fw",
    name: "key",
  },
  {
    icon: "fa-solid fa-thumbtack fa-fw",
    name: "thumbtack",
  },
  {
    icon: "fa-solid fa-gears fa-fw",
    name: "gears",
  },
  {
    icon: "fa-solid fa-paper-plane fa-fw",
    name: "paper-plane",
  },

  {
    icon: "fa-solid fa-code fa-fw",
    name: "code",
  },
  {
    icon: "fa-brands fa-squarespace fa-fw",
    name: "squarespace",
  },
  {
    icon: "fa-solid fa-globe fa-fw",
    name: "globe",
  },
  {
    icon: "fa-solid fa-truck fa-fw",
    name: "truck",
  },
  {
    icon: "fa-solid fa-city fa-fw",
    name: "city",
  },
  {
    icon: "fa-solid fa-ticket fa-fw",
    name: "ticket",
  },
  {
    icon: "fa-solid fa-tree fa-fw",
    name: "tree",
  },
  {
    icon: "fa-solid fa-wifi fa-fw",
    name: "wifi",
  },
  {
    icon: "fa-solid fa-paint-roller fa-fw",
    name: "paint-roller",
  },
  {
    icon: "fa-solid fa-bicycle fa-fw",
    name: "bicycle",
  },
  {
    icon: "fa-brands fa-android fa-fw",
    name: "android",
  },
  {
    icon: "fa-solid fa-sliders fa-fw",
    name: "sliders",
  },
  {
    icon: "fa-solid fa-brush fa-fw",
    name: "brush",
  },
  {
    icon: "fa-solid fa-hashtag fa-fw",
    name: "hashtag",
  },
  {
    icon: "fa-solid fa-flask fa-fw",
    name: "flask",
  },
  {
    icon: "fa-solid fa-briefcase fa-fw",
    name: "briefcase",
  },
  {
    icon: "fa-solid fa-compass fa-fw",
    name: "compass",
  },

  {
    icon: "fa-solid fa-dumpster-fire fa-fw",
    name: "dumpster-fire",
  },
  {
    icon: "fa-solid fa-person fa-fw",
    name: "person",
  },
  {
    icon: "fa-solid fa-person-dress fa-fw",
    name: "person-dress",
  },
  {
    icon: "fa-brands fa-shopify fa-fw",
    name: "shopify",
  },
  {
    icon: "fa-solid fa-address-book fa-fw",
    name: "address-book",
  },

  {
    icon: "fa-solid fa-bath fa-fw",
    name: "bath",
  },

  {
    icon: "fa-brands fa-medium fa-fw",
    name: "medium",
  },
  {
    icon: "fa-solid fa-snowflake fa-fw",
    name: "snowflake",
  },

  {
    icon: "fa-solid fa-right-to-bracket fa-fw",
    name: "right-to-bracket",
  },
  {
    icon: "fa-solid fa-earth-americas fa-fw",
    name: "earth-americas",
  },
  {
    icon: "fa-solid fa-cloud-arrow-up fa-fw",
    name: "cloud-arrow-up",
  },
  {
    icon: "fa-solid fa-binoculars fa-fw",
    name: "binoculars",
  },
  {
    icon: "fa-solid fa-palette fa-fw",
    name: "palette",
  },
  {
    icon: "fa-brands fa-codepen fa-fw",
    name: "codepen",
  },
  {
    icon: "fa-solid fa-layer-group fa-fw",
    name: "layer-group",
  },
  {
    icon: "fa-solid fa-users fa-fw",
    name: "users",
  },
  {
    icon: "fa-solid fa-gamepad fa-fw",
    name: "gamepad",
  },
  {
    icon: "fa-solid fa-business-time fa-fw",
    name: "business-time",
  },
  {
    icon: "fa-brands fa-cloudflare fa-fw",
    name: "cloudflare",
  },
  {
    icon: "fa-solid fa-feather fa-fw",
    name: "feather",
  },
  {
    icon: "fa-solid fa-sun fa-fw",
    name: "sun",
  },

  {
    icon: "fa-solid fa-link fa-fw",
    name: "link",
  },
  {
    icon: "fa-solid fa-pen-fancy fa-fw",
    name: "pen-fancy",
  },
  {
    icon: "fa-brands fa-airbnb fa-fw",
    name: "airbnb",
  },
  {
    icon: "fa-solid fa-fish fa-fw",
    name: "fish",
  },
  {
    icon: "fa-solid fa-bug fa-fw",
    name: "bug",
  },
  {
    icon: "fa-solid fa-shop fa-fw",
    name: "shop",
  },
  {
    icon: "fa-solid fa-mug-saucer fa-fw",
    name: "mug-saucer",
  },
  {
    icon: "fa-brands fa-vimeo fa-fw",
    name: "vimeo",
  },
  {
    icon: "fa-solid fa-landmark fa-fw",
    name: "landmark",
  },
  {
    icon: "fa-solid fa-poo-storm fa-fw",
    name: "poo-storm",
  },
  {
    icon: "fa-brands fa-whatsapp fa-fw",
    name: "whatsapp",
  },
  {
    icon: "fa-solid fa-chart-simple fa-fw",
    name: "chart-simple",
  },
  {
    icon: "fa-solid fa-shirt fa-fw",
    name: "shirt",
  },
  {
    icon: "fa-solid fa-anchor fa-fw",
    name: "anchor",
  },
  {
    icon: "fa-solid fa-quote-left fa-fw",
    name: "quote-left",
  },
  {
    icon: "fa-solid fa-bag-shopping fa-fw",
    name: "bag-shopping",
  },
  {
    icon: "fa-solid fa-gauge fa-fw",
    name: "gauge",
  },
  {
    icon: "fa-solid fa-code-compare fa-fw",
    name: "code-compare",
  },
  {
    icon: "fa-solid fa-user-secret fa-fw",
    name: "user-secret",
  },
  {
    icon: "fa-solid fa-stethoscope fa-fw",
    name: "stethoscope",
  },
  {
    icon: "fa-solid fa-car-side fa-fw",
    name: "car-side",
  },
  {
    icon: "fa-brands fa-intercom fa-fw",
    name: "intercom",
  },
  {
    icon: "fa-solid fa-truck-front fa-fw",
    name: "truck-front",
  },
  {
    icon: "fa-solid fa-cable-car fa-fw",
    name: "cable-car",
  },
  {
    icon: "fa-solid fa-mountain-sun fa-fw",
    name: "mountain-sun",
  },
  {
    icon: "fa-solid fa-location-pin fa-fw",
    name: "location-pin",
  },
  {
    icon: "fa-solid fa-info fa-fw",
    name: "info",
  },
  {
    icon: "fa-solid fa-user-minus fa-fw",
    name: "user-minus",
  },
  {
    icon: "fa-solid fa-calendar fa-fw",
    name: "calendar",
  },
  {
    icon: "fa-regular fa-calendar fa-fw",
    name: "calendar",
  },
  {
    icon: "fa-solid fa-cart-plus fa-fw",
    name: "cart-plus",
  },
  {
    icon: "fa-solid fa-clock fa-fw",
    name: "clock",
  },
  {
    icon: "fa-regular fa-clock fa-fw",
    name: "clock",
  },
  {
    icon: "fa-solid fa-circle fa-fw",
    name: "circle",
  },
  {
    icon: "fa-regular fa-circle fa-fw",
    name: "circle",
  },
  {
    icon: "fa-solid fa-play fa-fw",
    name: "play",
  },
  {
    icon: "fa-solid fa-cross fa-fw",
    name: "cross",
  },
  {
    icon: "fa-solid fa-backward fa-fw",
    name: "backward",
  },
  {
    icon: "fa-solid fa-chevron-up fa-fw",
    name: "chevron-up",
  },
  {
    icon: "fa-solid fa-passport fa-fw",
    name: "passport",
  },
  {
    icon: "fa-brands fa-usps fa-fw",
    name: "usps",
  },
  {
    icon: "fa-solid fa-question fa-fw",
    name: "question",
  },
  {
    icon: "fa-solid fa-pencil fa-fw",
    name: "pencil",
  },
  {
    icon: "fa-solid fa-phone-volume fa-fw",
    name: "phone-volume",
  },
  {
    icon: "fa-brands fa-wix fa-fw",
    name: "wix",
  },
  {
    icon: "fa-solid fa-upload fa-fw",
    name: "upload",
  },
  {
    icon: "fa-solid fa-strikethrough fa-fw",
    name: "strikethrough",
  },
  {
    icon: "fa-brands fa-line fa-fw",
    name: "line",
  },
  {
    icon: "fa-solid fa-credit-card fa-fw",
    name: "credit-card",
  },
  {
    icon: "fa-regular fa-credit-card fa-fw",
    name: "credit-card",
  },
  {
    icon: "fa-solid fa-street-view fa-fw",
    name: "street-view",
  },
  {
    icon: "fa-solid fa-database fa-fw",
    name: "database",
  },
  {
    icon: "fa-solid fa-copy fa-fw",
    name: "copy",
  },
  {
    icon: "fa-regular fa-copy fa-fw",
    name: "copy",
  },
  {
    icon: "fa-solid fa-mobile fa-fw",
    name: "mobile",
  },
  {
    icon: "fa-solid fa-square fa-fw",
    name: "square",
  },
  {
    icon: "fa-regular fa-square fa-fw",
    name: "square",
  },
  {
    icon: "fa-solid fa-sort fa-fw",
    name: "sort",
  },
  {
    icon: "fa-solid fa-forward fa-fw",
    name: "forward",
  },
  {
    icon: "fa-solid fa-hourglass-start fa-fw",
    name: "hourglass-start",
  },
  {
    icon: "fa-brands fa-behance fa-fw",
    name: "behance",
  },
  {
    icon: "fa-solid fa-newspaper fa-fw",
    name: "newspaper",
  },
  {
    icon: "fa-regular fa-newspaper fa-fw",
    name: "newspaper",
  },
  {
    icon: "fa-solid fa-notes-medical fa-fw",
    name: "notes-medical",
  },
  {
    icon: "fa-solid fa-table fa-fw",
    name: "table",
  },
  {
    icon: "fa-solid fa-building fa-fw",
    name: "building",
  },
  {
    icon: "fa-regular fa-building fa-fw",
    name: "building",
  },
  {
    icon: "fa-solid fa-stop fa-fw",
    name: "stop",
  },
  {
    icon: "fa-brands fa-openid fa-fw",
    name: "openid",
  },
  {
    icon: "fa-solid fa-store fa-fw",
    name: "store",
  },
  {
    icon: "fa-solid fa-flag fa-fw",
    name: "flag",
  },
  {
    icon: "fa-regular fa-flag fa-fw",
    name: "flag",
  },
  {
    icon: "fa-brands fa-product-hunt fa-fw",
    name: "product-hunt",
  },
  {
    icon: "fa-solid fa-file-excel fa-fw",
    name: "file-excel",
  },
  {
    icon: "fa-regular fa-file-excel fa-fw",
    name: "file-excel",
  },
  {
    icon: "fa-solid fa-network-wired fa-fw",
    name: "network-wired",
  },
  {
    icon: "fa-solid fa-cash-register fa-fw",
    name: "cash-register",
  },
  {
    icon: "fa-solid fa-file-export fa-fw",
    name: "file-export",
  },
  {
    icon: "fa-brands fa-internet-explorer fa-fw",
    name: "internet-explorer",
  },


  {
    icon: "fa-brands fa-pagelines fa-fw",
    name: "pagelines",
  },
  {
    icon: "fa-solid fa-angle-up fa-fw",
    name: "angle-up",
  },
  {
    icon: "fa-solid fa-shield fa-fw",
    name: "shield",
  },
  {
    icon: "fa-brands fa-teamspeak fa-fw",
    name: "teamspeak",
  },
  {
    icon: "fa-solid fa-address-card fa-fw",
    name: "address-card",
  },
  {
    icon: "fa-regular fa-address-card fa-fw",
    name: "address-card",
  },
  {
    icon: "fa-solid fa-expand fa-fw",
    name: "expand",
  },
  {
    icon: "fa-solid fa-flag-checkered fa-fw",
    name: "flag-checkered",
  },
  {
    icon: "fa-brands fa-html5 fa-fw",
    name: "html5",
  },
  {
    icon: "fa-solid fa-quote-right fa-fw",
    name: "quote-right",
  },
  {
    icon: "fa-solid fa-tags fa-fw",
    name: "tags",
  },
  {
    icon: "fa-solid fa-server fa-fw",
    name: "server",
  },
  {
    icon: "fa-solid fa-user-nurse fa-fw",
    name: "user-nurse",
  },
  {
    icon: "fa-solid fa-video-slash fa-fw",
    name: "video-slash",
  },
  {
    icon: "fa-solid fa-arrow-down fa-fw",
    name: "arrow-down",
  },
  {
    icon: "fa-solid fa-blog fa-fw",
    name: "blog",
  },
  {
    icon: "fa-solid fa-school fa-fw",
    name: "school",
  },
  {
    icon: "fa-solid fa-file-invoice fa-fw",
    name: "file-invoice",
  },
  {
    icon: "fa-solid fa-rocket fa-fw",
    name: "rocket",
  },
  {
    icon: "fa-solid fa-spinner fa-fw",
    name: "spinner",
  },
  {
    icon: "fa-brands fa-telegram fa-fw",
    name: "telegram",
  },
  {
    icon: "fa-solid fa-tty fa-fw",
    name: "tty",
  },
  {
    icon: "fa-solid fa-exclamation fa-fw",
    name: "exclamation",
  },
  {
    icon: "fa-solid fa-water fa-fw",
    name: "water",
  },
  {
    icon: "fa-solid fa-registered fa-fw",
    name: "registered",
  },
  {
    icon: "fa-regular fa-registered fa-fw",
    name: "registered",
  },
  {
    icon: "fa-solid fa-signature fa-fw",
    name: "signature",
  },
  {
    icon: "fa-solid fa-laptop fa-fw",
    name: "laptop",
  },
  {
    icon: "fa-solid fa-restroom fa-fw",
    name: "restroom",
  },
  {
    icon: "fa-solid fa-power-off fa-fw",
    name: "power-off",
  },
  {
    icon: "fa-solid fa-sitemap fa-fw",
    name: "sitemap",
  },
  {
    icon: "fa-solid fa-icons fa-fw",
    name: "icons",
  },
  {
    icon: "fa-solid fa-desktop fa-fw",
    name: "desktop",
  },
  {
    icon: "fa-solid fa-moon fa-fw",
    name: "moon",
  },
  {
    icon: "fa-regular fa-moon fa-fw",
    name: "moon",
  },
  {
    icon: "fa-solid fa-calendar-week fa-fw",
    name: "calendar-week",
  },
  {
    icon: "fa-brands fa-pinterest fa-fw",
    name: "pinterest",
  },
  {
    icon: "fa-solid fa-pause fa-fw",
    name: "pause",
  },
  {
    icon: "fa-solid fa-file-word fa-fw",
    name: "file-word",
  },
  {
    icon: "fa-regular fa-file-word fa-fw",
    name: "file-word",
  },
  {
    icon: "fa-solid fa-vials fa-fw",
    name: "vials",
  },
  {
    icon: "fa-solid fa-language fa-fw",
    name: "language",
  },
  {
    icon: "fa-solid fa-door-open fa-fw",
    name: "door-open",
  },
  {
    icon: "fa-solid fa-brain fa-fw",
    name: "brain",
  },
  {
    icon: "fa-solid fa-hotel fa-fw",
    name: "hotel",
  },
  {
    icon: "fa-solid fa-marker fa-fw",
    name: "marker",
  },
  {
    icon: "fa-solid fa-star-of-life fa-fw",
    name: "star-of-life",
  },
  {
    icon: "fa-solid fa-leaf fa-fw",
    name: "leaf",
  },
  {
    icon: "fa-solid fa-walkie-talkie fa-fw",
    name: "walkie-talkie",
  },
  {
    icon: "fa-solid fa-shower fa-fw",
    name: "shower",
  },
  {
    icon: "fa-brands fa-dashcube fa-fw",
    name: "dashcube",
  },
  {
    icon: "fa-solid fa-caret-down fa-fw",
    name: "caret-down",
  },
  {
    icon: "fa-brands fa-ideal fa-fw",
    name: "ideal",
  },
  {
    icon: "fa-brands fa-salesforce fa-fw",
    name: "salesforce",
  },
  {
    icon: "fa-solid fa-file-import fa-fw",
    name: "file-import",
  },
  {
    icon: "fa-solid fa-place-of-worship fa-fw",
    name: "place-of-worship",
  },
  {
    icon: "fa-solid fa-wallet fa-fw",
    name: "wallet",
  },
  {
    icon: "fa-solid fa-slash fa-fw",
    name: "slash",
  },
  {
    icon: "fa-brands fa-readme fa-fw",
    name: "readme",
  },
  {
    icon: "fa-solid fa-award fa-fw",
    name: "award",
  },
  {
    icon: "fa-solid fa-toggle-on fa-fw",
    name: "toggle-on",
  },
  {
    icon: "fa-solid fa-ship fa-fw",
    name: "ship",
  },
  {
    icon: "fa-brands fa-free-code-camp fa-fw",
    name: "free-code-camp",
  },
  {
    icon: "fa-brands fa-soundcloud fa-fw",
    name: "soundcloud",
  },
  {
    icon: "fa-solid fa-chalkboard fa-fw",
    name: "chalkboard",
  },
  {
    icon: "fa-brands fa-square-twitter fa-fw",
    name: "square-twitter",
  },
  {
    icon: "fa-solid fa-signal fa-fw",
    name: "signal",
  },
  {
    icon: "fa-solid fa-motorcycle fa-fw",
    name: "motorcycle",
  },
  {
    icon: "fa-solid fa-arrow-up-right-from-square fa-fw",
    name: "arrow-up-right-from-square",
  },
  {
    icon: "fa-solid fa-audio-description fa-fw",
    name: "audio-description",
  },
  {
    icon: "fa-brands fa-accessible-icon fa-fw",
    name: "accessible-icon",
  },
  {
    icon: "fa-solid fa-seedling fa-fw",
    name: "seedling",
  },
  {
    icon: "fa-solid fa-closed-captioning fa-fw",
    name: "closed-captioning",
  },
  {
    icon: "fa-regular fa-closed-captioning fa-fw",
    name: "closed-captioning",
  },
  {
    icon: "fa-solid fa-train fa-fw",
    name: "train",
  },
  {
    icon: "fa-brands fa-cc-visa fa-fw",
    name: "cc-visa",
  },
  {
    icon: "fa-solid fa-arrow-left fa-fw",
    name: "arrow-left",
  },
  {
    icon: "fa-solid fa-wrench fa-fw",
    name: "wrench",
  },
  {
    icon: "fa-solid fa-microchip fa-fw",
    name: "microchip",
  },
  {
    icon: "fa-solid fa-record-vinyl fa-fw",
    name: "record-vinyl",
  },
  {
    icon: "fa-brands fa-goodreads-g fa-fw",
    name: "goodreads-g",
  },
  {
    icon: "fa-solid fa-trophy fa-fw",
    name: "trophy",
  },
  {
    icon: "fa-solid fa-hammer fa-fw",
    name: "hammer",
  },
  {
    icon: "fa-solid fa-diamond fa-fw",
    name: "diamond",
  },
  {
    icon: "fa-solid fa-robot fa-fw",
    name: "robot",
  },
  {
    icon: "fa-solid fa-file-pdf fa-fw",
    name: "file-pdf",
  },
  {
    icon: "fa-regular fa-file-pdf fa-fw",
    name: "file-pdf",
  },
  {
    icon: "fa-brands fa-google-play fa-fw",
    name: "google-play",
  },
  {
    icon: "fa-solid fa-hospital fa-fw",
    name: "hospital",
  },
  {
    icon: "fa-regular fa-hospital fa-fw",
    name: "hospital",
  },
  {
    icon: "fa-solid fa-file-contract fa-fw",
    name: "file-contract",
  },
  {
    icon: "fa-solid fa-square-xmark fa-fw",
    name: "square-xmark",
  },
  {
    icon: "fa-solid fa-square-check fa-fw",
    name: "square-check",
  },
  {
    icon: "fa-regular fa-square-check fa-fw",
    name: "square-check",
  },
  {
    icon: "fa-solid fa-crown fa-fw",
    name: "crown",
  },
  {
    icon: "fa-brands fa-react fa-fw",
    name: "react",
  },
  {
    icon: "fa-solid fa-user-plus fa-fw",
    name: "user-plus",
  },
  {
    icon: "fa-solid fa-virus fa-fw",
    name: "virus",
  },
  {
    icon: "fa-solid fa-child fa-fw",
    name: "child",
  },
  {
    icon: "fa-solid fa-repeat fa-fw",
    name: "repeat",
  },
  {
    icon: "fa-solid fa-cube fa-fw",
    name: "cube",
  },
  {
    icon: "fa-solid fa-copyright fa-fw",
    name: "copyright",
  },
  {
    icon: "fa-regular fa-copyright fa-fw",
    name: "copyright",
  },
  {
    icon: "fa-solid fa-medal fa-fw",
    name: "medal",
  },
  {
    icon: "fa-solid fa-bullseye fa-fw",
    name: "bullseye",
  },
  {
    icon: "fa-solid fa-mask fa-fw",
    name: "mask",
  },
  {
    icon: "fa-solid fa-circle-check fa-fw",
    name: "circle-check",
  },
  {
    icon: "fa-regular fa-circle-check fa-fw",
    name: "circle-check",
  },
  {
    icon: "fa-solid fa-radio fa-fw",
    name: "radio",
  },
  {
    icon: "fa-solid fa-reply fa-fw",
    name: "reply",
  },
  {
    icon: "fa-solid fa-chair fa-fw",
    name: "chair",
  },
  {
    icon: "fa-solid fa-route fa-fw",
    name: "route",
  },
  {
    icon: "fa-brands fa-wikipedia-w fa-fw",
    name: "wikipedia-w",
  },
  {
    icon: "fa-solid fa-plug fa-fw",
    name: "plug",
  },
  {
    icon: "fa-solid fa-calculator fa-fw",
    name: "calculator",
  },
  {
    icon: "fa-solid fa-dragon fa-fw",
    name: "dragon",
  },
  {
    icon: "fa-solid fa-certificate fa-fw",
    name: "certificate",
  },
  {
    icon: "fa-solid fa-fingerprint fa-fw",
    name: "fingerprint",
  },
  {
    icon: "fa-solid fa-road fa-fw",
    name: "road",
  },
  {
    icon: "fa-solid fa-crosshairs fa-fw",
    name: "crosshairs",
  },
  {
    icon: "fa-solid fa-heading fa-fw",
    name: "heading",
  },
  {
    icon: "fa-solid fa-percent fa-fw",
    name: "percent",
  },
  {
    icon: "fa-brands fa-square-js fa-fw",
    name: "square-js",
  },
  {
    icon: "fa-solid fa-user-tie fa-fw",
    name: "user-tie",
  },
  {
    icon: "fa-brands fa-java fa-fw",
    name: "java",
  },
  {
    icon: "fa-solid fa-square-minus fa-fw",
    name: "square-minus",
  },
  {
    icon: "fa-regular fa-square-minus fa-fw",
    name: "square-minus",
  },
  {
    icon: "fa-solid fa-i-cursor fa-fw",
    name: "i-cursor",
  },
  {
    icon: "fa-solid fa-church fa-fw",
    name: "church",
  },
  {
    icon: "fa-solid fa-joint fa-fw",
    name: "joint",
  },
  {
    icon: "fa-solid fa-comments-dollar fa-fw",
    name: "comments-dollar",
  },

  {
    icon: "fa-solid fa-recycle fa-fw",
    name: "recycle",
  },
  {
    icon: "fa-brands fa-square-pinterest fa-fw",
    name: "square-pinterest",
  },
  {
    icon: "fa-solid fa-warehouse fa-fw",
    name: "warehouse",
  },
  {
    icon: "fa-solid fa-ruler fa-fw",
    name: "ruler",
  },
  {
    icon: "fa-brands fa-python fa-fw",
    name: "python",
  },
  {
    icon: "fa-solid fa-soap fa-fw",
    name: "soap",
  },
  {
    icon: "fa-solid fa-scroll fa-fw",
    name: "scroll",
  },
  {
    icon: "fa-brands fa-skype fa-fw",
    name: "skype",
  },
  {
    icon: "fa-solid fa-coins fa-fw",
    name: "coins",
  },
  {
    icon: "fa-solid fa-wind fa-fw",
    name: "wind",
  },
  {
    icon: "fa-solid fa-baby fa-fw",
    name: "baby",
  },
  {
    icon: "fa-solid fa-lightbulb fa-fw",
    name: "lightbulb",
  },
  {
    icon: "fa-regular fa-lightbulb fa-fw",
    name: "lightbulb",
  },
  {
    icon: "fa-brands fa-linux fa-fw",
    name: "linux",
  },
  {
    icon: "fa-brands fa-node fa-fw",
    name: "node",
  },
  {
    icon: "fa-brands fa-rebel fa-fw",
    name: "rebel",
  },
  {
    icon: "fa-solid fa-voicemail fa-fw",
    name: "voicemail",
  },
  {
    icon: "fa-solid fa-puzzle-piece fa-fw",
    name: "puzzle-piece",
  },
  {
    icon: "fa-solid fa-keyboard fa-fw",
    name: "keyboard",
  },
  {
    icon: "fa-regular fa-keyboard fa-fw",
    name: "keyboard",
  },
  {
    icon: "fa-solid fa-clone fa-fw",
    name: "clone",
  },
  {
    icon: "fa-regular fa-clone fa-fw",
    name: "clone",
  },
  {
    icon: "fa-solid fa-eraser fa-fw",
    name: "eraser",
  },
  {
    icon: "fa-solid fa-wine-bottle fa-fw",
    name: "wine-bottle",
  },
  {
    icon: "fa-solid fa-dice fa-fw",
    name: "dice",
  },
  {
    icon: "fa-solid fa-receipt fa-fw",
    name: "receipt",
  },
  {
    icon: "fa-solid fa-ring fa-fw",
    name: "ring",
  },
  {
    icon: "fa-brands fa-etsy fa-fw",
    name: "etsy",
  },
  {
    icon: "fa-solid fa-unlock fa-fw",
    name: "unlock",
  },
  {
    icon: "fa-brands fa-discourse fa-fw",
    name: "discourse",
  },
  {
    icon: "fa-solid fa-solar-panel fa-fw",
    name: "solar-panel",
  },
  {
    icon: "fa-solid fa-ruler-vertical fa-fw",
    name: "ruler-vertical",
  },
  {
    icon: "fa-solid fa-circle-notch fa-fw",
    name: "circle-notch",
  },
  {
    icon: "fa-solid fa-people-arrows fa-fw",
    name: "people-arrows",
  },
  {
    icon: "fa-solid fa-dollar-sign fa-fw",
    name: "dollar-sign",
  },
  {
    icon: "fa-brands fa-amazon fa-fw",
    name: "amazon",
  },
  {
    icon: "fa-solid fa-tablet fa-fw",
    name: "tablet",
  },
  {
    icon: "fa-solid fa-not-equal fa-fw",
    name: "not-equal",
  },
  {
    icon: "fa-solid fa-glasses fa-fw",
    name: "glasses",
  },
  {
    icon: "fa-solid fa-headset fa-fw",
    name: "headset",
  },
  {
    icon: "fa-solid fa-code-branch fa-fw",
    name: "code-branch",
  },
  {
    icon: "fa-brands fa-glide-g fa-fw",
    name: "glide-g",
  },
  {
    icon: "fa-solid fa-gopuram fa-fw",
    name: "gopuram",
  },
  {
    icon: "fa-solid fa-images fa-fw",
    name: "images",
  },
  {
    icon: "fa-regular fa-images fa-fw",
    name: "images",
  },
  {
    icon: "fa-solid fa-window-restore fa-fw",
    name: "window-restore",
  },
  {
    icon: "fa-regular fa-window-restore fa-fw",
    name: "window-restore",
  },
  {
    icon: "fa-solid fa-industry fa-fw",
    name: "industry",
  },
  {
    icon: "fa-brands fa-gitlab fa-fw",
    name: "gitlab",
  },
  {
    icon: "fa-brands fa-spotify fa-fw",
    name: "spotify",
  },
  {
    icon: "fa-solid fa-stamp fa-fw",
    name: "stamp",
  },
  {
    icon: "fa-solid fa-microphone-slash fa-fw",
    name: "microphone-slash",
  },
  {
    icon: "fa-brands fa-think-peaks fa-fw",
    name: "think-peaks",
  },
  {
    icon: "fa-brands fa-microsoft fa-fw",
    name: "microsoft",
  },
  {
    icon: "fa-solid fa-cookie-bite fa-fw",
    name: "cookie-bite",
  },
  {
    icon: "fa-solid fa-otter fa-fw",
    name: "otter",
  },
  {
    icon: "fa-solid fa-chevron-down fa-fw",
    name: "chevron-down",
  },
  {
    icon: "fa-solid fa-kiwi-bird fa-fw",
    name: "kiwi-bird",
  },
  {
    icon: "fa-solid fa-viruses fa-fw",
    name: "viruses",
  },
  {
    icon: "fa-brands fa-elementor fa-fw",
    name: "elementor",
  },
  {
    icon: "fa-brands fa-pied-piper fa-fw",
    name: "pied-piper",
  },
  {
    icon: "fa-brands fa-square-youtube fa-fw",
    name: "square-youtube",
  },
  {
    icon: "fa-solid fa-umbrella-beach fa-fw",
    name: "umbrella-beach",
  },
  {
    icon: "fa-solid fa-subscript fa-fw",
    name: "subscript",
  },
  {
    icon: "fa-solid fa-tablets fa-fw",
    name: "tablets",
  },
  {
    icon: "fa-brands fa-cc-mastercard fa-fw",
    name: "cc-mastercard",
  },
  {
    icon: "fa-brands fa-facebook-messenger fa-fw",
    name: "facebook-messenger",
  },
  {
    icon: "fa-brands fa-atlassian fa-fw",
    name: "atlassian",
  },
  {
    icon: "fa-brands fa-playstation fa-fw",
    name: "playstation",
  },
  {
    icon: "fa-brands fa-fly fa-fw",
    name: "fly",
  },
  {
    icon: "fa-solid fa-microphone fa-fw",
    name: "microphone",
  },
  {
    icon: "fa-brands fa-meetup fa-fw",
    name: "meetup",
  },

  {
    icon: "fa-solid fa-dumbbell fa-fw",
    name: "dumbbell",
  },
  {
    icon: "fa-brands fa-twitch fa-fw",
    name: "twitch",
  },
  {
    icon: "fa-solid fa-plane-departure fa-fw",
    name: "plane-departure",
  },
  {
    icon: "fa-brands fa-waze fa-fw",
    name: "waze",
  },
  {
    icon: "fa-solid fa-z fa-fw",
    name: "z",
  },
  {
    icon: "fa-solid fa-yin-yang fa-fw",
    name: "yin-yang",
  },
  {
    icon: "fa-solid fa-yen-sign fa-fw",
    name: "yen-sign",
  },
  {
    icon: "fa-solid fa-y fa-fw",
    name: "y",
  },
  {
    icon: "fa-solid fa-xmarks-lines fa-fw",
    name: "xmarks-lines",
  },
  {
    icon: "fa-solid fa-x-ray fa-fw",
    name: "x-ray",
  },
  {
    icon: "fa-solid fa-x fa-fw",
    name: "x",
  },
  {
    icon: "fa-solid fa-worm fa-fw",
    name: "worm",
  },
  {
    icon: "fa-solid fa-won-sign fa-fw",
    name: "won-sign",
  },
  {
    icon: "fa-solid fa-wine-glass-empty fa-fw",
    name: "wine-glass-empty",
  },
  {
    icon: "fa-solid fa-wine-glass fa-fw",
    name: "wine-glass",
  },
  {
    icon: "fa-solid fa-window-minimize fa-fw",
    name: "window-minimize",
  },
  {
    icon: "fa-solid fa-window-maximize fa-fw",
    name: "window-maximize",
  },
  {
    icon: "fa-solid fa-whiskey-glass fa-fw",
    name: "whiskey-glass",
  },
  {
    icon: "fa-solid fa-wheelchair-move fa-fw",
    name: "wheelchair-move",
  },
  {
    icon: "fa-solid fa-wheelchair fa-fw",
    name: "wheelchair",
  },
  {
    icon: "fa-solid fa-wheat-awn-circle-exclamation fa-fw",
    name: "wheat-awn-circle-exclamation",
  },
  {
    icon: "fa-solid fa-wheat-awn fa-fw",
    name: "wheat-awn",
  },
  {
    icon: "fa-solid fa-weight-scale fa-fw",
    name: "weight-scale",
  },
  {
    icon: "fa-solid fa-weight-hanging fa-fw",
    name: "weight-hanging",
  },
  {
    icon: "fa-solid fa-wave-square fa-fw",
    name: "wave-square",
  },
  {
    icon: "fa-solid fa-water-ladder fa-fw",
    name: "water-ladder",
  },
  {
    icon: "fa-solid fa-wand-sparkles fa-fw",
    name: "wand-sparkles",
  },
  {
    icon: "fa-solid fa-wand-magic fa-fw",
    name: "wand-magic",
  },
  {
    icon: "fa-solid fa-w fa-fw",
    name: "w",
  },
  {
    icon: "fa-solid fa-vr-cardboard fa-fw",
    name: "vr-cardboard",
  },
  {
    icon: "fa-solid fa-volume-xmark fa-fw",
    name: "volume-xmark",
  },
  {
    icon: "fa-solid fa-volume-off fa-fw",
    name: "volume-off",
  },
  {
    icon: "fa-solid fa-volume-low fa-fw",
    name: "volume-low",
  },
  {
    icon: "fa-solid fa-volume-high fa-fw",
    name: "volume-high",
  },
  {
    icon: "fa-solid fa-volleyball fa-fw",
    name: "volleyball",
  },
  {
    icon: "fa-solid fa-volcano fa-fw",
    name: "volcano",
  },
  {
    icon: "fa-solid fa-virus-slash fa-fw",
    name: "virus-slash",
  },
  {
    icon: "fa-solid fa-virus-covid-slash fa-fw",
    name: "virus-covid-slash",
  },
  {
    icon: "fa-solid fa-virus-covid fa-fw",
    name: "virus-covid",
  },
  {
    icon: "fa-solid fa-vihara fa-fw",
    name: "vihara",
  },
  {
    icon: "fa-solid fa-vial-virus fa-fw",
    name: "vial-virus",
  },
  {
    icon: "fa-solid fa-vial-circle-check fa-fw",
    name: "vial-circle-check",
  },
  {
    icon: "fa-solid fa-vial fa-fw",
    name: "vial",
  },
  {
    icon: "fa-solid fa-vest-patches fa-fw",
    name: "vest-patches",
  },
  {
    icon: "fa-solid fa-vest fa-fw",
    name: "vest",
  },
  {
    icon: "fa-solid fa-venus-mars fa-fw",
    name: "venus-mars",
  },
  {
    icon: "fa-solid fa-venus-double fa-fw",
    name: "venus-double",
  },
  {
    icon: "fa-solid fa-venus fa-fw",
    name: "venus",
  },
  {
    icon: "fa-solid fa-vector-square fa-fw",
    name: "vector-square",
  },
  {
    icon: "fa-solid fa-vault fa-fw",
    name: "vault",
  },
  {
    icon: "fa-solid fa-van-shuttle fa-fw",
    name: "van-shuttle",
  },
  {
    icon: "fa-solid fa-v fa-fw",
    name: "v",
  },
  {
    icon: "fa-solid fa-utensils fa-fw",
    name: "utensils",
  },
  {
    icon: "fa-solid fa-users-viewfinder fa-fw",
    name: "users-viewfinder",
  },
  {
    icon: "fa-solid fa-users-slash fa-fw",
    name: "users-slash",
  },
  {
    icon: "fa-solid fa-users-rectangle fa-fw",
    name: "users-rectangle",
  },
  {
    icon: "fa-solid fa-users-rays fa-fw",
    name: "users-rays",
  },
  {
    icon: "fa-solid fa-users-line fa-fw",
    name: "users-line",
  },
  {
    icon: "fa-solid fa-users-gear fa-fw",
    name: "users-gear",
  },
  {
    icon: "fa-solid fa-users-between-lines fa-fw",
    name: "users-between-lines",
  },
  {
    icon: "fa-solid fa-user-xmark fa-fw",
    name: "user-xmark",
  },
  {
    icon: "fa-solid fa-user-tag fa-fw",
    name: "user-tag",
  },
  {
    icon: "fa-solid fa-user-slash fa-fw",
    name: "user-slash",
  },
  {
    icon: "fa-solid fa-user-shield fa-fw",
    name: "user-shield",
  },
  {
    icon: "fa-solid fa-user-pen fa-fw",
    name: "user-pen",
  },
  {
    icon: "fa-solid fa-user-ninja fa-fw",
    name: "user-ninja",
  },
  {
    icon: "fa-solid fa-user-lock fa-fw",
    name: "user-lock",
  },
  {
    icon: "fa-solid fa-user-large-slash fa-fw",
    name: "user-large-slash",
  },
  {
    icon: "fa-solid fa-user-large fa-fw",
    name: "user-large",
  },
  {
    icon: "fa-solid fa-user-injured fa-fw",
    name: "user-injured",
  },
  {
    icon: "fa-solid fa-user-group fa-fw",
    name: "user-group",
  },
  {
    icon: "fa-solid fa-user-graduate fa-fw",
    name: "user-graduate",
  },
  {
    icon: "fa-solid fa-user-gear fa-fw",
    name: "user-gear",
  },
  {
    icon: "fa-solid fa-user-doctor fa-fw",
    name: "user-doctor",
  },
  {
    icon: "fa-solid fa-user-clock fa-fw",
    name: "user-clock",
  },
  {
    icon: "fa-solid fa-user-check fa-fw",
    name: "user-check",
  },
  {
    icon: "fa-solid fa-user-astronaut fa-fw",
    name: "user-astronaut",
  },
  {
    icon: "fa-solid fa-up-right-from-square fa-fw",
    name: "up-right-from-square",
  },
  {
    icon: "fa-solid fa-up-right-and-down-left-from-center fa-fw",
    name: "up-right-and-down-left-from-center",
  },
  {
    icon: "fa-solid fa-up-long fa-fw",
    name: "up-long",
  },
  {
    icon: "fa-solid fa-up-down-left-right fa-fw",
    name: "up-down-left-right",
  },
  {
    icon: "fa-solid fa-up-down fa-fw",
    name: "up-down",
  },
  {
    icon: "fa-solid fa-unlock-keyhole fa-fw",
    name: "unlock-keyhole",
  },
  {
    icon: "fa-solid fa-universal-access fa-fw",
    name: "universal-access",
  },
  {
    icon: "fa-solid fa-underline fa-fw",
    name: "underline",
  },
  {
    icon: "fa-solid fa-u fa-fw",
    name: "u",
  },
  {
    icon: "fa-solid fa-tv fa-fw",
    name: "tv",
  },
  {
    icon: "fa-solid fa-turn-up fa-fw",
    name: "turn-up",
  },
  {
    icon: "fa-solid fa-turn-down fa-fw",
    name: "turn-down",
  },
  {
    icon: "fa-solid fa-turkish-lira-sign fa-fw",
    name: "turkish-lira-sign",
  },
  {
    icon: "fa-solid fa-truck-ramp-box fa-fw",
    name: "truck-ramp-box",
  },
  {
    icon: "fa-solid fa-truck-plane fa-fw",
    name: "truck-plane",
  },
  {
    icon: "fa-solid fa-truck-pickup fa-fw",
    name: "truck-pickup",
  },
  {
    icon: "fa-solid fa-truck-moving fa-fw",
    name: "truck-moving",
  },
  {
    icon: "fa-solid fa-truck-medical fa-fw",
    name: "truck-medical",
  },
  {
    icon: "fa-solid fa-truck-field-un fa-fw",
    name: "truck-field-un",
  },
  {
    icon: "fa-solid fa-truck-field fa-fw",
    name: "truck-field",
  },
  {
    icon: "fa-solid fa-truck-droplet fa-fw",
    name: "truck-droplet",
  },
  {
    icon: "fa-solid fa-truck-arrow-right fa-fw",
    name: "truck-arrow-right",
  },
  {
    icon: "fa-solid fa-trowel-bricks fa-fw",
    name: "trowel-bricks",
  },
  {
    icon: "fa-solid fa-trowel fa-fw",
    name: "trowel",
  },
  {
    icon: "fa-solid fa-triangle-exclamation fa-fw",
    name: "triangle-exclamation",
  },
  {
    icon: "fa-solid fa-tree-city fa-fw",
    name: "tree-city",
  },
  {
    icon: "fa-solid fa-trash-can-arrow-up fa-fw",
    name: "trash-can-arrow-up",
  },
  {
    icon: "fa-solid fa-trash-can fa-fw",
    name: "trash-can",
  },
  {
    icon: "fa-solid fa-trash-arrow-up fa-fw",
    name: "trash-arrow-up",
  },
  {
    icon: "fa-solid fa-transgender fa-fw",
    name: "transgender",
  },
  {
    icon: "fa-solid fa-train-tram fa-fw",
    name: "train-tram",
  },
  {
    icon: "fa-solid fa-train-subway fa-fw",
    name: "train-subway",
  },
  {
    icon: "fa-solid fa-trailer fa-fw",
    name: "trailer",
  },
  {
    icon: "fa-solid fa-traffic-light fa-fw",
    name: "traffic-light",
  },
  {
    icon: "fa-solid fa-trademark fa-fw",
    name: "trademark",
  },
  {
    icon: "fa-solid fa-tractor fa-fw",
    name: "tractor",
  },
  {
    icon: "fa-solid fa-tower-observation fa-fw",
    name: "tower-observation",
  },
  {
    icon: "fa-solid fa-tower-cell fa-fw",
    name: "tower-cell",
  },
  {
    icon: "fa-solid fa-tower-broadcast fa-fw",
    name: "tower-broadcast",
  },
  {
    icon: "fa-solid fa-tornado fa-fw",
    name: "tornado",
  },
  {
    icon: "fa-solid fa-torii-gate fa-fw",
    name: "torii-gate",
  },
  {
    icon: "fa-solid fa-tooth fa-fw",
    name: "tooth",
  },
  {
    icon: "fa-solid fa-toolbox fa-fw",
    name: "toolbox",
  },
  {
    icon: "fa-solid fa-toilets-portable fa-fw",
    name: "toilets-portable",
  },
  {
    icon: "fa-solid fa-toilet-portable fa-fw",
    name: "toilet-portable",
  },
  {
    icon: "fa-solid fa-toilet-paper-slash fa-fw",
    name: "toilet-paper-slash",
  },
  {
    icon: "fa-solid fa-toilet-paper fa-fw",
    name: "toilet-paper",
  },
  {
    icon: "fa-solid fa-toilet fa-fw",
    name: "toilet",
  },
  {
    icon: "fa-solid fa-toggle-off fa-fw",
    name: "toggle-off",
  },
  {
    icon: "fa-solid fa-timeline fa-fw",
    name: "timeline",
  },
  {
    icon: "fa-solid fa-ticket-simple fa-fw",
    name: "ticket-simple",
  },
  {
    icon: "fa-solid fa-thermometer fa-fw",
    name: "thermometer",
  },
  {
    icon: "fa-solid fa-text-width fa-fw",
    name: "text-width",
  },
  {
    icon: "fa-solid fa-text-slash fa-fw",
    name: "text-slash",
  },
  {
    icon: "fa-solid fa-text-height fa-fw",
    name: "text-height",
  },
  {
    icon: "fa-solid fa-terminal fa-fw",
    name: "terminal",
  },
  {
    icon: "fa-solid fa-tents fa-fw",
    name: "tents",
  },
  {
    icon: "fa-solid fa-tent-arrows-down fa-fw",
    name: "tent-arrows-down",
  },
  {
    icon: "fa-solid fa-tent-arrow-turn-left fa-fw",
    name: "tent-arrow-turn-left",
  },
  {
    icon: "fa-solid fa-tent-arrow-left-right fa-fw",
    name: "tent-arrow-left-right",
  },
  {
    icon: "fa-solid fa-tent-arrow-down-to-line fa-fw",
    name: "tent-arrow-down-to-line",
  },
  {
    icon: "fa-solid fa-tent fa-fw",
    name: "tent",
  },
  {
    icon: "fa-solid fa-tenge-sign fa-fw",
    name: "tenge-sign",
  },
  {
    icon: "fa-solid fa-temperature-three-quarters fa-fw",
    name: "temperature-three-quarters",
  },
  {
    icon: "fa-solid fa-temperature-quarter fa-fw",
    name: "temperature-quarter",
  },
  {
    icon: "fa-solid fa-temperature-low fa-fw",
    name: "temperature-low",
  },
  {
    icon: "fa-solid fa-temperature-high fa-fw",
    name: "temperature-high",
  },
  {
    icon: "fa-solid fa-temperature-half fa-fw",
    name: "temperature-half",
  },
  {
    icon: "fa-solid fa-temperature-full fa-fw",
    name: "temperature-full",
  },
  {
    icon: "fa-solid fa-temperature-empty fa-fw",
    name: "temperature-empty",
  },
  {
    icon: "fa-solid fa-temperature-arrow-up fa-fw",
    name: "temperature-arrow-up",
  },
  {
    icon: "fa-solid fa-temperature-arrow-down fa-fw",
    name: "temperature-arrow-down",
  },
  {
    icon: "fa-solid fa-teeth-open fa-fw",
    name: "teeth-open",
  },
  {
    icon: "fa-solid fa-teeth fa-fw",
    name: "teeth",
  },
  {
    icon: "fa-solid fa-taxi fa-fw",
    name: "taxi",
  },
  {
    icon: "fa-solid fa-tarp-droplet fa-fw",
    name: "tarp-droplet",
  },
  {
    icon: "fa-solid fa-tarp fa-fw",
    name: "tarp",
  },
  {
    icon: "fa-solid fa-tape fa-fw",
    name: "tape",
  },
  {
    icon: "fa-solid fa-tachograph-digital fa-fw",
    name: "tachograph-digital",
  },
  {
    icon: "fa-solid fa-tablet-screen-button fa-fw",
    name: "tablet-screen-button",
  },
  {
    icon: "fa-solid fa-tablet-button fa-fw",
    name: "tablet-button",
  },
  {
    icon: "fa-solid fa-table-tennis-paddle-ball fa-fw",
    name: "table-tennis-paddle-ball",
  },
  {
    icon: "fa-solid fa-table-list fa-fw",
    name: "table-list",
  },
  {
    icon: "fa-solid fa-table-columns fa-fw",
    name: "table-columns",
  },
  {
    icon: "fa-solid fa-table-cells-large fa-fw",
    name: "table-cells-large",
  },
  {
    icon: "fa-solid fa-table-cells fa-fw",
    name: "table-cells",
  },
  {
    icon: "fa-solid fa-t fa-fw",
    name: "t",
  },
  {
    icon: "fa-solid fa-syringe fa-fw",
    name: "syringe",
  },
  {
    icon: "fa-solid fa-synagogue fa-fw",
    name: "synagogue",
  },
  {
    icon: "fa-solid fa-swatchbook fa-fw",
    name: "swatchbook",
  },
  {
    icon: "fa-solid fa-superscript fa-fw",
    name: "superscript",
  },
  {
    icon: "fa-solid fa-sun-plant-wilt fa-fw",
    name: "sun-plant-wilt",
  },
  {
    icon: "fa-solid fa-suitcase-rolling fa-fw",
    name: "suitcase-rolling",
  },
  {
    icon: "fa-solid fa-suitcase-medical fa-fw",
    name: "suitcase-medical",
  },
  {
    icon: "fa-solid fa-suitcase fa-fw",
    name: "suitcase",
  },
  {
    icon: "fa-solid fa-stroopwafel fa-fw",
    name: "stroopwafel",
  },
  {
    icon: "fa-solid fa-store-slash fa-fw",
    name: "store-slash",
  },
  {
    icon: "fa-solid fa-stopwatch-20 fa-fw",
    name: "stopwatch-20",
  },
  {
    icon: "fa-solid fa-stopwatch fa-fw",
    name: "stopwatch",
  },
  {
    icon: "fa-solid fa-sterling-sign fa-fw",
    name: "sterling-sign",
  },
  {
    icon: "fa-solid fa-star-of-david fa-fw",
    name: "star-of-david",
  },
  {
    icon: "fa-solid fa-star-half-stroke fa-fw",
    name: "star-half-stroke",
  },
  {
    icon: "fa-solid fa-star-half fa-fw",
    name: "star-half",
  },
  {
    icon: "fa-solid fa-star-and-crescent fa-fw",
    name: "star-and-crescent",
  },
  {
    icon: "fa-solid fa-stapler fa-fw",
    name: "stapler",
  },
  {
    icon: "fa-solid fa-stairs fa-fw",
    name: "stairs",
  },
  {
    icon: "fa-solid fa-staff-snake fa-fw",
    name: "staff-snake",
  },
  {
    icon: "fa-solid fa-square-virus fa-fw",
    name: "square-virus",
  },
  {
    icon: "fa-solid fa-square-up-right fa-fw",
    name: "square-up-right",
  },
  {
    icon: "fa-solid fa-square-share-nodes fa-fw",
    name: "square-share-nodes",
  },
  {
    icon: "fa-solid fa-square-rss fa-fw",
    name: "square-rss",
  },
  {
    icon: "fa-solid fa-square-root-variable fa-fw",
    name: "square-root-variable",
  },
  {
    icon: "fa-solid fa-square-poll-vertical fa-fw",
    name: "square-poll-vertical",
  },
  {
    icon: "fa-solid fa-square-poll-horizontal fa-fw",
    name: "square-poll-horizontal",
  },
  {
    icon: "fa-solid fa-square-plus fa-fw",
    name: "square-plus",
  },
  {
    icon: "fa-solid fa-square-phone-flip fa-fw",
    name: "square-phone-flip",
  },
  {
    icon: "fa-solid fa-square-phone fa-fw",
    name: "square-phone",
  },
  {
    icon: "fa-solid fa-square-person-confined fa-fw",
    name: "square-person-confined",
  },
  {
    icon: "fa-solid fa-square-pen fa-fw",
    name: "square-pen",
  },
  {
    icon: "fa-solid fa-square-parking fa-fw",
    name: "square-parking",
  },
  {
    icon: "fa-solid fa-square-nfi fa-fw",
    name: "square-nfi",
  },
  {
    icon: "fa-solid fa-square-h fa-fw",
    name: "square-h",
  },
  {
    icon: "fa-solid fa-square-full fa-fw",
    name: "square-full",
  },
  {
    icon: "fa-solid fa-square-envelope fa-fw",
    name: "square-envelope",
  },
  {
    icon: "fa-solid fa-square-caret-up fa-fw",
    name: "square-caret-up",
  },
  {
    icon: "fa-solid fa-square-caret-right fa-fw",
    name: "square-caret-right",
  },
  {
    icon: "fa-solid fa-square-caret-left fa-fw",
    name: "square-caret-left",
  },
  {
    icon: "fa-solid fa-square-caret-down fa-fw",
    name: "square-caret-down",
  },
  {
    icon: "fa-solid fa-square-arrow-up-right fa-fw",
    name: "square-arrow-up-right",
  },
  {
    icon: "fa-solid fa-spray-can-sparkles fa-fw",
    name: "spray-can-sparkles",
  },
  {
    icon: "fa-solid fa-spray-can fa-fw",
    name: "spray-can",
  },
  {
    icon: "fa-solid fa-spoon fa-fw",
    name: "spoon",
  },
  {
    icon: "fa-solid fa-splotch fa-fw",
    name: "splotch",
  },
  {
    icon: "fa-solid fa-spider fa-fw",
    name: "spider",
  },
  {
    icon: "fa-solid fa-spell-check fa-fw",
    name: "spell-check",
  },
  {
    icon: "fa-solid fa-sort-up fa-fw",
    name: "sort-up",
  },
  {
    icon: "fa-solid fa-sort-down fa-fw",
    name: "sort-down",
  },
  {
    icon: "fa-solid fa-socks fa-fw",
    name: "socks",
  },
  {
    icon: "fa-solid fa-snowplow fa-fw",
    name: "snowplow",
  },
  {
    icon: "fa-solid fa-snowman fa-fw",
    name: "snowman",
  },
  {
    icon: "fa-solid fa-smoking fa-fw",
    name: "smoking",
  },
  {
    icon: "fa-solid fa-smog fa-fw",
    name: "smog",
  },
  {
    icon: "fa-solid fa-sleigh fa-fw",
    name: "sleigh",
  },
  {
    icon: "fa-solid fa-sink fa-fw",
    name: "sink",
  },
  {
    icon: "fa-solid fa-sim-card fa-fw",
    name: "sim-card",
  },
  {
    icon: "fa-solid fa-signs-post fa-fw",
    name: "signs-post",
  },
  {
    icon: "fa-solid fa-sign-hanging fa-fw",
    name: "sign-hanging",
  },
  {
    icon: "fa-solid fa-shuttle-space fa-fw",
    name: "shuttle-space",
  },
  {
    icon: "fa-solid fa-shuffle fa-fw",
    name: "shuffle",
  },
  {
    icon: "fa-solid fa-shrimp fa-fw",
    name: "shrimp",
  },
  {
    icon: "fa-solid fa-shop-slash fa-fw",
    name: "shop-slash",
  },
  {
    icon: "fa-solid fa-shop-lock fa-fw",
    name: "shop-lock",
  },
  {
    icon: "fa-solid fa-shoe-prints fa-fw",
    name: "shoe-prints",
  },
  {
    icon: "fa-solid fa-shield-virus fa-fw",
    name: "shield-virus",
  },
  {
    icon: "fa-solid fa-shield-heart fa-fw",
    name: "shield-heart",
  },
  {
    icon: "fa-solid fa-shield-dog fa-fw",
    name: "shield-dog",
  },
  {
    icon: "fa-solid fa-shield-cat fa-fw",
    name: "shield-cat",
  },
  {
    icon: "fa-solid fa-shekel-sign fa-fw",
    name: "shekel-sign",
  },
  {
    icon: "fa-solid fa-sheet-plastic fa-fw",
    name: "sheet-plastic",
  },
  {
    icon: "fa-solid fa-share-nodes fa-fw",
    name: "share-nodes",
  },
  {
    icon: "fa-solid fa-shapes fa-fw",
    name: "shapes",
  },
  {
    icon: "fa-solid fa-section fa-fw",
    name: "section",
  },
  {
    icon: "fa-solid fa-sd-card fa-fw",
    name: "sd-card",
  },
  {
    icon: "fa-solid fa-scroll-torah fa-fw",
    name: "scroll-torah",
  },
  {
    icon: "fa-solid fa-screwdriver-wrench fa-fw",
    name: "screwdriver-wrench",
  },
  {
    icon: "fa-solid fa-screwdriver fa-fw",
    name: "screwdriver",
  },
  {
    icon: "fa-solid fa-scissors fa-fw",
    name: "scissors",
  },
  {
    icon: "fa-solid fa-school-lock fa-fw",
    name: "school-lock",
  },
  {
    icon: "fa-solid fa-school-flag fa-fw",
    name: "school-flag",
  },
  {
    icon: "fa-solid fa-school-circle-xmark fa-fw",
    name: "school-circle-xmark",
  },
  {
    icon: "fa-solid fa-school-circle-exclamation fa-fw",
    name: "school-circle-exclamation",
  },
  {
    icon: "fa-solid fa-school-circle-check fa-fw",
    name: "school-circle-check",
  },
  {
    icon: "fa-solid fa-scale-unbalanced-flip fa-fw",
    name: "scale-unbalanced-flip",
  },
  {
    icon: "fa-solid fa-scale-unbalanced fa-fw",
    name: "scale-unbalanced",
  },
  {
    icon: "fa-solid fa-scale-balanced fa-fw",
    name: "scale-balanced",
  },
  {
    icon: "fa-solid fa-satellite-dish fa-fw",
    name: "satellite-dish",
  },
  {
    icon: "fa-solid fa-satellite fa-fw",
    name: "satellite",
  },
  {
    icon: "fa-solid fa-sailboat fa-fw",
    name: "sailboat",
  },
  {
    icon: "fa-solid fa-sack-xmark fa-fw",
    name: "sack-xmark",
  },
  {
    icon: "fa-solid fa-sack-dollar fa-fw",
    name: "sack-dollar",
  },
  {
    icon: "fa-solid fa-s fa-fw",
    name: "s",
  },
  {
    icon: "fa-solid fa-rupiah-sign fa-fw",
    name: "rupiah-sign",
  },
  {
    icon: "fa-solid fa-rupee-sign fa-fw",
    name: "rupee-sign",
  },
  {
    icon: "fa-solid fa-ruler-horizontal fa-fw",
    name: "ruler-horizontal",
  },
  {
    icon: "fa-solid fa-ruler-combined fa-fw",
    name: "ruler-combined",
  },
  {
    icon: "fa-solid fa-rug fa-fw",
    name: "rug",
  },
  {
    icon: "fa-solid fa-ruble-sign fa-fw",
    name: "ruble-sign",
  },
  {
    icon: "fa-solid fa-rss fa-fw",
    name: "rss",
  },
  {
    icon: "fa-solid fa-rotate-left fa-fw",
    name: "rotate-left",
  },
  {
    icon: "fa-solid fa-rotate fa-fw",
    name: "rotate",
  },
  {
    icon: "fa-solid fa-road-spikes fa-fw",
    name: "road-spikes",
  },
  {
    icon: "fa-solid fa-road-lock fa-fw",
    name: "road-lock",
  },
  {
    icon: "fa-solid fa-road-circle-xmark fa-fw",
    name: "road-circle-xmark",
  },
  {
    icon: "fa-solid fa-road-circle-exclamation fa-fw",
    name: "road-circle-exclamation",
  },
  {
    icon: "fa-solid fa-road-circle-check fa-fw",
    name: "road-circle-check",
  },
  {
    icon: "fa-solid fa-road-barrier fa-fw",
    name: "road-barrier",
  },
  {
    icon: "fa-solid fa-right-long fa-fw",
    name: "right-long",
  },
  {
    icon: "fa-solid fa-right-left fa-fw",
    name: "right-left",
  },
  {
    icon: "fa-solid fa-right-from-bracket fa-fw",
    name: "right-from-bracket",
  },
  {
    icon: "fa-solid fa-ribbon fa-fw",
    name: "ribbon",
  },
  {
    icon: "fa-solid fa-retweet fa-fw",
    name: "retweet",
  },
  {
    icon: "fa-solid fa-republican fa-fw",
    name: "republican",
  },
  {
    icon: "fa-solid fa-reply-all fa-fw",
    name: "reply-all",
  },
  {
    icon: "fa-solid fa-rectangle-xmark fa-fw",
    name: "rectangle-xmark",
  },
  {
    icon: "fa-solid fa-rectangle-list fa-fw",
    name: "rectangle-list",
  },
  {
    icon: "fa-solid fa-rectangle-ad fa-fw",
    name: "rectangle-ad",
  },
  {
    icon: "fa-solid fa-ranking-star fa-fw",
    name: "ranking-star",
  },
  {
    icon: "fa-solid fa-rainbow fa-fw",
    name: "rainbow",
  },
  {
    icon: "fa-solid fa-radiation fa-fw",
    name: "radiation",
  },
  {
    icon: "fa-solid fa-r fa-fw",
    name: "r",
  },
  {
    icon: "fa-solid fa-qrcode fa-fw",
    name: "qrcode",
  },
  {
    icon: "fa-solid fa-q fa-fw",
    name: "q",
  },
  {
    icon: "fa-solid fa-pump-soap fa-fw",
    name: "pump-soap",
  },
  {
    icon: "fa-solid fa-pump-medical fa-fw",
    name: "pump-medical",
  },
  {
    icon: "fa-solid fa-prescription-bottle-medical fa-fw",
    name: "prescription-bottle-medical",
  },
  {
    icon: "fa-solid fa-prescription-bottle fa-fw",
    name: "prescription-bottle",
  },
  {
    icon: "fa-solid fa-prescription fa-fw",
    name: "prescription",
  },
  {
    icon: "fa-solid fa-poop fa-fw",
    name: "poop",
  },
  {
    icon: "fa-solid fa-podcast fa-fw",
    name: "podcast",
  },
  {
    icon: "fa-solid fa-plus-minus fa-fw",
    name: "plus-minus",
  },
  {
    icon: "fa-solid fa-plug-circle-xmark fa-fw",
    name: "plug-circle-xmark",
  },
  {
    icon: "fa-solid fa-plug-circle-plus fa-fw",
    name: "plug-circle-plus",
  },
  {
    icon: "fa-solid fa-plug-circle-minus fa-fw",
    name: "plug-circle-minus",
  },
  {
    icon: "fa-solid fa-plug-circle-exclamation fa-fw",
    name: "plug-circle-exclamation",
  },
  {
    icon: "fa-solid fa-plug-circle-check fa-fw",
    name: "plug-circle-check",
  },
  {
    icon: "fa-solid fa-plug-circle-bolt fa-fw",
    name: "plug-circle-bolt",
  },
  {
    icon: "fa-solid fa-plate-wheat fa-fw",
    name: "plate-wheat",
  },
  {
    icon: "fa-solid fa-plant-wilt fa-fw",
    name: "plant-wilt",
  },
  {
    icon: "fa-solid fa-plane-up fa-fw",
    name: "plane-up",
  },
  {
    icon: "fa-solid fa-plane-slash fa-fw",
    name: "plane-slash",
  },
  {
    icon: "fa-solid fa-plane-lock fa-fw",
    name: "plane-lock",
  },
  {
    icon: "fa-solid fa-plane-circle-xmark fa-fw",
    name: "plane-circle-xmark",
  },
  {
    icon: "fa-solid fa-plane-circle-exclamation fa-fw",
    name: "plane-circle-exclamation",
  },
  {
    icon: "fa-solid fa-plane-circle-check fa-fw",
    name: "plane-circle-check",
  },
  {
    icon: "fa-solid fa-plane-arrival fa-fw",
    name: "plane-arrival",
  },
  {
    icon: "fa-solid fa-pizza-slice fa-fw",
    name: "pizza-slice",
  },
  {
    icon: "fa-solid fa-pills fa-fw",
    name: "pills",
  },
  {
    icon: "fa-solid fa-piggy-bank fa-fw",
    name: "piggy-bank",
  },
  {
    icon: "fa-solid fa-photo-film fa-fw",
    name: "photo-film",
  },
  {
    icon: "fa-solid fa-phone-slash fa-fw",
    name: "phone-slash",
  },
  {
    icon: "fa-solid fa-phone-flip fa-fw",
    name: "phone-flip",
  },
  {
    icon: "fa-solid fa-peso-sign fa-fw",
    name: "peso-sign",
  },
  {
    icon: "fa-solid fa-peseta-sign fa-fw",
    name: "peseta-sign",
  },
  {
    icon: "fa-solid fa-person-walking-with-cane fa-fw",
    name: "person-walking-with-cane",
  },
  {
    icon: "fa-solid fa-person-walking-luggage fa-fw",
    name: "person-walking-luggage",
  },
  {
    icon: "fa-solid fa-person-walking-dashed-line-arrow-right fa-fw",
    name: "person-walking-dashed-line-arrow-right",
  },
  {
    icon: "fa-solid fa-person-walking-arrow-right fa-fw",
    name: "person-walking-arrow-right",
  },
  {
    icon: "fa-solid fa-person-walking-arrow-loop-left fa-fw",
    name: "person-walking-arrow-loop-left",
  },
  {
    icon: "fa-solid fa-person-walking fa-fw",
    name: "person-walking",
  },
  {
    icon: "fa-solid fa-person-through-window fa-fw",
    name: "person-through-window",
  },
  {
    icon: "fa-solid fa-person-swimming fa-fw",
    name: "person-swimming",
  },
  {
    icon: "fa-solid fa-person-snowboarding fa-fw",
    name: "person-snowboarding",
  },
  {
    icon: "fa-solid fa-person-skiing-nordic fa-fw",
    name: "person-skiing-nordic",
  },
  {
    icon: "fa-solid fa-person-skiing fa-fw",
    name: "person-skiing",
  },
  {
    icon: "fa-solid fa-person-skating fa-fw",
    name: "person-skating",
  },
  {
    icon: "fa-solid fa-person-shelter fa-fw",
    name: "person-shelter",
  },
  {
    icon: "fa-solid fa-person-running fa-fw",
    name: "person-running",
  },
  {
    icon: "fa-solid fa-person-rifle fa-fw",
    name: "person-rifle",
  },
  {
    icon: "fa-solid fa-person-rays fa-fw",
    name: "person-rays",
  },
  {
    icon: "fa-solid fa-person-pregnant fa-fw",
    name: "person-pregnant",
  },
  {
    icon: "fa-solid fa-person-praying fa-fw",
    name: "person-praying",
  },
  {
    icon: "fa-solid fa-person-military-to-person fa-fw",
    name: "person-military-to-person",
  },
  {
    icon: "fa-solid fa-person-military-rifle fa-fw",
    name: "person-military-rifle",
  },
  {
    icon: "fa-solid fa-person-military-pointing fa-fw",
    name: "person-military-pointing",
  },
  {
    icon: "fa-solid fa-person-hiking fa-fw",
    name: "person-hiking",
  },
  {
    icon: "fa-solid fa-person-harassing fa-fw",
    name: "person-harassing",
  },
  {
    icon: "fa-solid fa-person-half-dress fa-fw",
    name: "person-half-dress",
  },
  {
    icon: "fa-solid fa-person-falling-burst fa-fw",
    name: "person-falling-burst",
  },
  {
    icon: "fa-solid fa-person-falling fa-fw",
    name: "person-falling",
  },
  {
    icon: "fa-solid fa-person-drowning fa-fw",
    name: "person-drowning",
  },
  {
    icon: "fa-solid fa-person-dress-burst fa-fw",
    name: "person-dress-burst",
  },
  {
    icon: "fa-solid fa-person-dots-from-line fa-fw",
    name: "person-dots-from-line",
  },
  {
    icon: "fa-solid fa-person-digging fa-fw",
    name: "person-digging",
  },
  {
    icon: "fa-solid fa-person-circle-xmark fa-fw",
    name: "person-circle-xmark",
  },
  {
    icon: "fa-solid fa-person-circle-question fa-fw",
    name: "person-circle-question",
  },
  {
    icon: "fa-solid fa-person-circle-plus fa-fw",
    name: "person-circle-plus",
  },
  {
    icon: "fa-solid fa-person-circle-minus fa-fw",
    name: "person-circle-minus",
  },
  {
    icon: "fa-solid fa-person-circle-exclamation fa-fw",
    name: "person-circle-exclamation",
  },
  {
    icon: "fa-solid fa-person-circle-check fa-fw",
    name: "person-circle-check",
  },
  {
    icon: "fa-solid fa-person-chalkboard fa-fw",
    name: "person-chalkboard",
  },
  {
    icon: "fa-solid fa-person-cane fa-fw",
    name: "person-cane",
  },
  {
    icon: "fa-solid fa-person-burst fa-fw",
    name: "person-burst",
  },
  {
    icon: "fa-solid fa-person-breastfeeding fa-fw",
    name: "person-breastfeeding",
  },
  {
    icon: "fa-solid fa-person-booth fa-fw",
    name: "person-booth",
  },
  {
    icon: "fa-solid fa-person-biking fa-fw",
    name: "person-biking",
  },
  {
    icon: "fa-solid fa-person-arrow-up-from-line fa-fw",
    name: "person-arrow-up-from-line",
  },
  {
    icon: "fa-solid fa-person-arrow-down-to-line fa-fw",
    name: "person-arrow-down-to-line",
  },
  {
    icon: "fa-solid fa-pepper-hot fa-fw",
    name: "pepper-hot",
  },
  {
    icon: "fa-solid fa-people-roof fa-fw",
    name: "people-roof",
  },
  {
    icon: "fa-solid fa-people-robbery fa-fw",
    name: "people-robbery",
  },
  {
    icon: "fa-solid fa-people-pulling fa-fw",
    name: "people-pulling",
  },
  {
    icon: "fa-solid fa-people-line fa-fw",
    name: "people-line",
  },
  {
    icon: "fa-solid fa-people-group fa-fw",
    name: "people-group",
  },
  {
    icon: "fa-solid fa-people-carry-box fa-fw",
    name: "people-carry-box",
  },
  {
    icon: "fa-solid fa-pen-ruler fa-fw",
    name: "pen-ruler",
  },
  {
    icon: "fa-solid fa-pen-clip fa-fw",
    name: "pen-clip",
  },
  {
    icon: "fa-solid fa-peace fa-fw",
    name: "peace",
  },
  {
    icon: "fa-solid fa-paw fa-fw",
    name: "paw",
  },
  {
    icon: "fa-solid fa-paste fa-fw",
    name: "paste",
  },
  {
    icon: "fa-solid fa-paragraph fa-fw",
    name: "paragraph",
  },
  {
    icon: "fa-solid fa-parachute-box fa-fw",
    name: "parachute-box",
  },
  {
    icon: "fa-solid fa-panorama fa-fw",
    name: "panorama",
  },
  {
    icon: "fa-solid fa-pallet fa-fw",
    name: "pallet",
  },
  {
    icon: "fa-solid fa-paintbrush fa-fw",
    name: "paintbrush",
  },
  {
    icon: "fa-solid fa-pager fa-fw",
    name: "pager",
  },
  {
    icon: "fa-solid fa-p fa-fw",
    name: "p",
  },
  {
    icon: "fa-solid fa-outdent fa-fw",
    name: "outdent",
  },
  {
    icon: "fa-solid fa-om fa-fw",
    name: "om",
  },
  {
    icon: "fa-solid fa-oil-well fa-fw",
    name: "oil-well",
  },
  {
    icon: "fa-solid fa-oil-can fa-fw",
    name: "oil-can",
  },
  {
    icon: "fa-solid fa-object-ungroup fa-fw",
    name: "object-ungroup",
  },
  {
    icon: "fa-solid fa-object-group fa-fw",
    name: "object-group",
  },
  {
    icon: "fa-solid fa-o fa-fw",
    name: "o",
  },
  {
    icon: "fa-solid fa-note-sticky fa-fw",
    name: "note-sticky",
  },
  {
    icon: "fa-solid fa-neuter fa-fw",
    name: "neuter",
  },
  {
    icon: "fa-solid fa-naira-sign fa-fw",
    name: "naira-sign",
  },
  {
    icon: "fa-solid fa-n fa-fw",
    name: "n",
  },
  {
    icon: "fa-solid fa-mountain-city fa-fw",
    name: "mountain-city",
  },
  {
    icon: "fa-solid fa-mountain fa-fw",
    name: "mountain",
  },
  {
    icon: "fa-solid fa-mound fa-fw",
    name: "mound",
  },
  {
    icon: "fa-solid fa-mosquito-net fa-fw",
    name: "mosquito-net",
  },
  {
    icon: "fa-solid fa-mosquito fa-fw",
    name: "mosquito",
  },
  {
    icon: "fa-solid fa-mosque fa-fw",
    name: "mosque",
  },
  {
    icon: "fa-solid fa-mortar-pestle fa-fw",
    name: "mortar-pestle",
  },
  {
    icon: "fa-solid fa-monument fa-fw",
    name: "monument",
  },
  {
    icon: "fa-solid fa-money-check-dollar fa-fw",
    name: "money-check-dollar",
  },
  {
    icon: "fa-solid fa-money-check fa-fw",
    name: "money-check",
  },
  {
    icon: "fa-solid fa-money-bills fa-fw",
    name: "money-bills",
  },
  {
    icon: "fa-solid fa-money-bill-wheat fa-fw",
    name: "money-bill-wheat",
  },
  {
    icon: "fa-solid fa-money-bill-wave fa-fw",
    name: "money-bill-wave",
  },
  {
    icon: "fa-solid fa-money-bill-trend-up fa-fw",
    name: "money-bill-trend-up",
  },
  {
    icon: "fa-solid fa-money-bill-transfer fa-fw",
    name: "money-bill-transfer",
  },
  {
    icon: "fa-solid fa-money-bill-1-wave fa-fw",
    name: "money-bill-1-wave",
  },
  {
    icon: "fa-solid fa-money-bill-1 fa-fw",
    name: "money-bill-1",
  },
  {
    icon: "fa-solid fa-mobile-screen-button fa-fw",
    name: "mobile-screen-button",
  },
  {
    icon: "fa-solid fa-mobile-screen fa-fw",
    name: "mobile-screen",
  },
  {
    icon: "fa-solid fa-mobile-retro fa-fw",
    name: "mobile-retro",
  },
  {
    icon: "fa-solid fa-mobile-button fa-fw",
    name: "mobile-button",
  },
  {
    icon: "fa-solid fa-mitten fa-fw",
    name: "mitten",
  },
  {
    icon: "fa-solid fa-minimize fa-fw",
    name: "minimize",
  },
  {
    icon: "fa-solid fa-mill-sign fa-fw",
    name: "mill-sign",
  },
  {
    icon: "fa-solid fa-microscope fa-fw",
    name: "microscope",
  },
  {
    icon: "fa-solid fa-microphone-lines-slash fa-fw",
    name: "microphone-lines-slash",
  },
  {
    icon: "fa-solid fa-microphone-lines fa-fw",
    name: "microphone-lines",
  },
  {
    icon: "fa-solid fa-meteor fa-fw",
    name: "meteor",
  },
  {
    icon: "fa-solid fa-message fa-fw",
    name: "message",
  },
  {
    icon: "fa-solid fa-mercury fa-fw",
    name: "mercury",
  },
  {
    icon: "fa-solid fa-menorah fa-fw",
    name: "menorah",
  },
  {
    icon: "fa-solid fa-memory fa-fw",
    name: "memory",
  },
  {
    icon: "fa-solid fa-maximize fa-fw",
    name: "maximize",
  },
  {
    icon: "fa-solid fa-mattress-pillow fa-fw",
    name: "mattress-pillow",
  },
  {
    icon: "fa-solid fa-masks-theater fa-fw",
    name: "masks-theater",
  },
  {
    icon: "fa-solid fa-mask-ventilator fa-fw",
    name: "mask-ventilator",
  },
  {
    icon: "fa-solid fa-mask-face fa-fw",
    name: "mask-face",
  },
  {
    icon: "fa-solid fa-martini-glass-empty fa-fw",
    name: "martini-glass-empty",
  },
  {
    icon: "fa-solid fa-martini-glass-citrus fa-fw",
    name: "martini-glass-citrus",
  },
  {
    icon: "fa-solid fa-martini-glass fa-fw",
    name: "martini-glass",
  },
  {
    icon: "fa-solid fa-mars-stroke-up fa-fw",
    name: "mars-stroke-up",
  },
  {
    icon: "fa-solid fa-mars-stroke-right fa-fw",
    name: "mars-stroke-right",
  },
  {
    icon: "fa-solid fa-mars-stroke fa-fw",
    name: "mars-stroke",
  },
  {
    icon: "fa-solid fa-mars-double fa-fw",
    name: "mars-double",
  },
  {
    icon: "fa-solid fa-mars-and-venus-burst fa-fw",
    name: "mars-and-venus-burst",
  },
  {
    icon: "fa-solid fa-mars-and-venus fa-fw",
    name: "mars-and-venus",
  },
  {
    icon: "fa-solid fa-mars fa-fw",
    name: "mars",
  },
  {
    icon: "fa-solid fa-map-pin fa-fw",
    name: "map-pin",
  },
  {
    icon: "fa-solid fa-map-location-dot fa-fw",
    name: "map-location-dot",
  },
  {
    icon: "fa-solid fa-map-location fa-fw",
    name: "map-location",
  },
  {
    icon: "fa-solid fa-map fa-fw",
    name: "map",
  },
  {
    icon: "fa-solid fa-manat-sign fa-fw",
    name: "manat-sign",
  },
  {
    icon: "fa-solid fa-magnifying-glass-plus fa-fw",
    name: "magnifying-glass-plus",
  },
  {
    icon: "fa-solid fa-magnifying-glass-minus fa-fw",
    name: "magnifying-glass-minus",
  },
  {
    icon: "fa-solid fa-magnifying-glass-location fa-fw",
    name: "magnifying-glass-location",
  },
  {
    icon: "fa-solid fa-magnifying-glass-dollar fa-fw",
    name: "magnifying-glass-dollar",
  },
  {
    icon: "fa-solid fa-magnifying-glass-chart fa-fw",
    name: "magnifying-glass-chart",
  },
  {
    icon: "fa-solid fa-magnifying-glass-arrow-right fa-fw",
    name: "magnifying-glass-arrow-right",
  },
  {
    icon: "fa-solid fa-m fa-fw",
    name: "m",
  },
  {
    icon: "fa-solid fa-lungs-virus fa-fw",
    name: "lungs-virus",
  },
  {
    icon: "fa-solid fa-lungs fa-fw",
    name: "lungs",
  },
  {
    icon: "fa-solid fa-locust fa-fw",
    name: "locust",
  },
  {
    icon: "fa-solid fa-lock-open fa-fw",
    name: "lock-open",
  },
  {
    icon: "fa-solid fa-location-pin-lock fa-fw",
    name: "location-pin-lock",
  },
  {
    icon: "fa-solid fa-location-crosshairs fa-fw",
    name: "location-crosshairs",
  },
  {
    icon: "fa-solid fa-location-arrow fa-fw",
    name: "location-arrow",
  },
  {
    icon: "fa-solid fa-litecoin-sign fa-fw",
    name: "litecoin-sign",
  },
  {
    icon: "fa-solid fa-list-ul fa-fw",
    name: "list-ul",
  },
  {
    icon: "fa-solid fa-list-ol fa-fw",
    name: "list-ol",
  },
  {
    icon: "fa-solid fa-list-check fa-fw",
    name: "list-check",
  },
  {
    icon: "fa-solid fa-lira-sign fa-fw",
    name: "lira-sign",
  },
  {
    icon: "fa-solid fa-link-slash fa-fw",
    name: "link-slash",
  },
  {
    icon: "fa-solid fa-lines-leaning fa-fw",
    name: "lines-leaning",
  },
  {
    icon: "fa-solid fa-life-ring fa-fw",
    name: "life-ring",
  },
  {
    icon: "fa-solid fa-less-than-equal fa-fw",
    name: "less-than-equal",
  },
  {
    icon: "fa-solid fa-less-than fa-fw",
    name: "less-than",
  },
  {
    icon: "fa-solid fa-left-right fa-fw",
    name: "left-right",
  },
  {
    icon: "fa-solid fa-left-long fa-fw",
    name: "left-long",
  },
  {
    icon: "fa-solid fa-lari-sign fa-fw",
    name: "lari-sign",
  },
  {
    icon: "fa-solid fa-laptop-medical fa-fw",
    name: "laptop-medical",
  },
  {
    icon: "fa-solid fa-laptop-file fa-fw",
    name: "laptop-file",
  },
  {
    icon: "fa-solid fa-laptop-code fa-fw",
    name: "laptop-code",
  },
  {
    icon: "fa-solid fa-landmark-flag fa-fw",
    name: "landmark-flag",
  },
  {
    icon: "fa-solid fa-landmark-dome fa-fw",
    name: "landmark-dome",
  },
  {
    icon: "fa-solid fa-land-mine-on fa-fw",
    name: "land-mine-on",
  },
  {
    icon: "fa-solid fa-l fa-fw",
    name: "l",
  },
  {
    icon: "fa-solid fa-kitchen-set fa-fw",
    name: "kitchen-set",
  },
  {
    icon: "fa-solid fa-kit-medical fa-fw",
    name: "kit-medical",
  },
  {
    icon: "fa-solid fa-kip-sign fa-fw",
    name: "kip-sign",
  },

  {
    icon: "fa-solid fa-kaaba fa-fw",
    name: "kaaba",
  },
  {
    icon: "fa-solid fa-k fa-fw",
    name: "k",
  },
  {
    icon: "fa-solid fa-jug-detergent fa-fw",
    name: "jug-detergent",
  },
  {
    icon: "fa-solid fa-jet-fighter-up fa-fw",
    name: "jet-fighter-up",
  },
  {
    icon: "fa-solid fa-jet-fighter fa-fw",
    name: "jet-fighter",
  },
  {
    icon: "fa-solid fa-jedi fa-fw",
    name: "jedi",
  },
  {
    icon: "fa-solid fa-jar-wheat fa-fw",
    name: "jar-wheat",
  },
  {
    icon: "fa-solid fa-jar fa-fw",
    name: "jar",
  },
  {
    icon: "fa-solid fa-j fa-fw",
    name: "j",
  },
  {
    icon: "fa-solid fa-italic fa-fw",
    name: "italic",
  },
  {
    icon: "fa-solid fa-infinity fa-fw",
    name: "infinity",
  },
  {
    icon: "fa-solid fa-indian-rupee-sign fa-fw",
    name: "indian-rupee-sign",
  },
  {
    icon: "fa-solid fa-indent fa-fw",
    name: "indent",
  },
  {
    icon: "fa-solid fa-image-portrait fa-fw",
    name: "image-portrait",
  },
  {
    icon: "fa-solid fa-igloo fa-fw",
    name: "igloo",
  },
  {
    icon: "fa-solid fa-id-card-clip fa-fw",
    name: "id-card-clip",
  },
  {
    icon: "fa-solid fa-id-card fa-fw",
    name: "id-card",
  },
  {
    icon: "fa-solid fa-id-badge fa-fw",
    name: "id-badge",
  },
  {
    icon: "fa-solid fa-icicles fa-fw",
    name: "icicles",
  },
  {
    icon: "fa-solid fa-ice-cream fa-fw",
    name: "ice-cream",
  },
  {
    icon: "fa-solid fa-i fa-fw",
    name: "i",
  },
  {
    icon: "fa-solid fa-hurricane fa-fw",
    name: "hurricane",
  },
  {
    icon: "fa-solid fa-hryvnia-sign fa-fw",
    name: "hryvnia-sign",
  },
  {
    icon: "fa-solid fa-house-user fa-fw",
    name: "house-user",
  },
  {
    icon: "fa-solid fa-house-tsunami fa-fw",
    name: "house-tsunami",
  },
  {
    icon: "fa-solid fa-house-signal fa-fw",
    name: "house-signal",
  },
  {
    icon: "fa-solid fa-house-medical-flag fa-fw",
    name: "house-medical-flag",
  },
  {
    icon: "fa-solid fa-house-medical-circle-xmark fa-fw",
    name: "house-medical-circle-xmark",
  },
  {
    icon: "fa-solid fa-house-medical-circle-exclamation fa-fw",
    name: "house-medical-circle-exclamation",
  },
  {
    icon: "fa-solid fa-house-medical-circle-check fa-fw",
    name: "house-medical-circle-check",
  },
  {
    icon: "fa-solid fa-house-medical fa-fw",
    name: "house-medical",
  },
  {
    icon: "fa-solid fa-house-lock fa-fw",
    name: "house-lock",
  },
  {
    icon: "fa-solid fa-house-laptop fa-fw",
    name: "house-laptop",
  },
  {
    icon: "fa-solid fa-house-flood-water-circle-arrow-right fa-fw",
    name: "house-flood-water-circle-arrow-right",
  },
  {
    icon: "fa-solid fa-house-flood-water fa-fw",
    name: "house-flood-water",
  },
  {
    icon: "fa-solid fa-house-flag fa-fw",
    name: "house-flag",
  },
  {
    icon: "fa-solid fa-house-fire fa-fw",
    name: "house-fire",
  },
  {
    icon: "fa-solid fa-house-crack fa-fw",
    name: "house-crack",
  },
  {
    icon: "fa-solid fa-house-circle-xmark fa-fw",
    name: "house-circle-xmark",
  },
  {
    icon: "fa-solid fa-house-circle-exclamation fa-fw",
    name: "house-circle-exclamation",
  },
  {
    icon: "fa-solid fa-house-circle-check fa-fw",
    name: "house-circle-check",
  },
  {
    icon: "fa-solid fa-house-chimney-window fa-fw",
    name: "house-chimney-window",
  },
  {
    icon: "fa-solid fa-house-chimney-user fa-fw",
    name: "house-chimney-user",
  },
  {
    icon: "fa-solid fa-house-chimney-medical fa-fw",
    name: "house-chimney-medical",
  },
  {
    icon: "fa-solid fa-house-chimney-crack fa-fw",
    name: "house-chimney-crack",
  },
  {
    icon: "fa-solid fa-house-chimney fa-fw",
    name: "house-chimney",
  },
  {
    icon: "fa-solid fa-hourglass-half fa-fw",
    name: "hourglass-half",
  },
  {
    icon: "fa-solid fa-hourglass-end fa-fw",
    name: "hourglass-end",
  },
  {
    icon: "fa-solid fa-hourglass fa-fw",
    name: "hourglass",
  },
  {
    icon: "fa-solid fa-hotdog fa-fw",
    name: "hotdog",
  },
  {
    icon: "fa-solid fa-hot-tub-person fa-fw",
    name: "hot-tub-person",
  },
  {
    icon: "fa-solid fa-hospital-user fa-fw",
    name: "hospital-user",
  },
  {
    icon: "fa-solid fa-horse-head fa-fw",
    name: "horse-head",
  },
  {
    icon: "fa-solid fa-horse fa-fw",
    name: "horse",
  },
  {
    icon: "fa-solid fa-holly-berry fa-fw",
    name: "holly-berry",
  },
  {
    icon: "fa-solid fa-hockey-puck fa-fw",
    name: "hockey-puck",
  },
  {
    icon: "fa-solid fa-hill-rockslide fa-fw",
    name: "hill-rockslide",
  },
  {
    icon: "fa-solid fa-hill-avalanche fa-fw",
    name: "hill-avalanche",
  },
  {
    icon: "fa-solid fa-highlighter fa-fw",
    name: "highlighter",
  },
  {
    icon: "fa-solid fa-helmet-un fa-fw",
    name: "helmet-un",
  },
  {
    icon: "fa-solid fa-helmet-safety fa-fw",
    name: "helmet-safety",
  },
  {
    icon: "fa-solid fa-helicopter-symbol fa-fw",
    name: "helicopter-symbol",
  },
  {
    icon: "fa-solid fa-helicopter fa-fw",
    name: "helicopter",
  },
  {
    icon: "fa-solid fa-heart-pulse fa-fw",
    name: "heart-pulse",
  },
  {
    icon: "fa-solid fa-heart-crack fa-fw",
    name: "heart-crack",
  },
  {
    icon: "fa-solid fa-heart-circle-xmark fa-fw",
    name: "heart-circle-xmark",
  },
  {
    icon: "fa-solid fa-heart-circle-plus fa-fw",
    name: "heart-circle-plus",
  },
  {
    icon: "fa-solid fa-heart-circle-minus fa-fw",
    name: "heart-circle-minus",
  },
  {
    icon: "fa-solid fa-heart-circle-exclamation fa-fw",
    name: "heart-circle-exclamation",
  },
  {
    icon: "fa-solid fa-heart-circle-check fa-fw",
    name: "heart-circle-check",
  },
  {
    icon: "fa-solid fa-heart-circle-bolt fa-fw",
    name: "heart-circle-bolt",
  },
  {
    icon: "fa-solid fa-headphones-simple fa-fw",
    name: "headphones-simple",
  },
  {
    icon: "fa-solid fa-head-side-virus fa-fw",
    name: "head-side-virus",
  },
  {
    icon: "fa-solid fa-head-side-mask fa-fw",
    name: "head-side-mask",
  },
  {
    icon: "fa-solid fa-head-side-cough-slash fa-fw",
    name: "head-side-cough-slash",
  },
  {
    icon: "fa-solid fa-head-side-cough fa-fw",
    name: "head-side-cough",
  },
  {
    icon: "fa-solid fa-hat-wizard fa-fw",
    name: "hat-wizard",
  },
  {
    icon: "fa-solid fa-hat-cowboy-side fa-fw",
    name: "hat-cowboy-side",
  },
  {
    icon: "fa-solid fa-hat-cowboy fa-fw",
    name: "hat-cowboy",
  },
  {
    icon: "fa-solid fa-hard-drive fa-fw",
    name: "hard-drive",
  },
  {
    icon: "fa-solid fa-hanukiah fa-fw",
    name: "hanukiah",
  },
  {
    icon: "fa-solid fa-hamsa fa-fw",
    name: "hamsa",
  },
  {
    icon: "fa-solid fa-h fa-fw",
    name: "h",
  },
  {
    icon: "fa-solid fa-gun fa-fw",
    name: "gun",
  },
  {
    icon: "fa-solid fa-guitar fa-fw",
    name: "guitar",
  },
  {
    icon: "fa-solid fa-guarani-sign fa-fw",
    name: "guarani-sign",
  },
  {
    icon: "fa-solid fa-group-arrows-rotate fa-fw",
    name: "group-arrows-rotate",
  },
  {
    icon: "fa-solid fa-grip-vertical fa-fw",
    name: "grip-vertical",
  },
  {
    icon: "fa-solid fa-grip-lines-vertical fa-fw",
    name: "grip-lines-vertical",
  },
  {
    icon: "fa-solid fa-grip-lines fa-fw",
    name: "grip-lines",
  },
  {
    icon: "fa-solid fa-grip fa-fw",
    name: "grip",
  },
  {
    icon: "fa-solid fa-greater-than-equal fa-fw",
    name: "greater-than-equal",
  },
  {
    icon: "fa-solid fa-greater-than fa-fw",
    name: "greater-than",
  },
  {
    icon: "fa-solid fa-graduation-cap fa-fw",
    name: "graduation-cap",
  },
  {
    icon: "fa-solid fa-golf-ball-tee fa-fw",
    name: "golf-ball-tee",
  },
  {
    icon: "fa-solid fa-glass-water-droplet fa-fw",
    name: "glass-water-droplet",
  },
  {
    icon: "fa-solid fa-glass-water fa-fw",
    name: "glass-water",
  },
  {
    icon: "fa-solid fa-gifts fa-fw",
    name: "gifts",
  },
  {
    icon: "fa-solid fa-genderless fa-fw",
    name: "genderless",
  },
  {
    icon: "fa-solid fa-gem fa-fw",
    name: "gem",
  },
  {
    icon: "fa-solid fa-gavel fa-fw",
    name: "gavel",
  },
  {
    icon: "fa-solid fa-gauge-simple-high fa-fw",
    name: "gauge-simple-high",
  },
  {
    icon: "fa-solid fa-gauge-simple fa-fw",
    name: "gauge-simple",
  },
  {
    icon: "fa-solid fa-gauge-high fa-fw",
    name: "gauge-high",
  },
  {
    icon: "fa-solid fa-gas-pump fa-fw",
    name: "gas-pump",
  },
  {
    icon: "fa-solid fa-g fa-fw",
    name: "g",
  },
  {
    icon: "fa-solid fa-futbol fa-fw",
    name: "futbol",
  },
  {
    icon: "fa-solid fa-frog fa-fw",
    name: "frog",
  },
  {
    icon: "fa-solid fa-franc-sign fa-fw",
    name: "franc-sign",
  },
  {
    icon: "fa-solid fa-forward-step fa-fw",
    name: "forward-step",
  },
  {
    icon: "fa-solid fa-forward-fast fa-fw",
    name: "forward-fast",
  },
  {
    icon: "fa-solid fa-football fa-fw",
    name: "football",
  },
  {
    icon: "fa-solid fa-font-awesome fa-fw",
    name: "font-awesome",
  },
  {
    icon: "fa-solid fa-folder-tree fa-fw",
    name: "folder-tree",
  },
  {
    icon: "fa-solid fa-folder-plus fa-fw",
    name: "folder-plus",
  },
  {
    icon: "fa-solid fa-folder-minus fa-fw",
    name: "folder-minus",
  },
  {
    icon: "fa-solid fa-folder-closed fa-fw",
    name: "folder-closed",
  },
  {
    icon: "fa-solid fa-florin-sign fa-fw",
    name: "florin-sign",
  },
  {
    icon: "fa-solid fa-floppy-disk fa-fw",
    name: "floppy-disk",
  },
  {
    icon: "fa-solid fa-flask-vial fa-fw",
    name: "flask-vial",
  },
  {
    icon: "fa-solid fa-flag-usa fa-fw",
    name: "flag-usa",
  },
  {
    icon: "fa-solid fa-fish-fins fa-fw",
    name: "fish-fins",
  },
  {
    icon: "fa-solid fa-fire-flame-simple fa-fw",
    name: "fire-flame-simple",
  },
  {
    icon: "fa-solid fa-fire-flame-curved fa-fw",
    name: "fire-flame-curved",
  },
  {
    icon: "fa-solid fa-fire-extinguisher fa-fw",
    name: "fire-extinguisher",
  },
  {
    icon: "fa-solid fa-fire-burner fa-fw",
    name: "fire-burner",
  },
  {
    icon: "fa-solid fa-filter-circle-xmark fa-fw",
    name: "filter-circle-xmark",
  },
  {
    icon: "fa-solid fa-filter-circle-dollar fa-fw",
    name: "filter-circle-dollar",
  },
  {
    icon: "fa-solid fa-fill-drip fa-fw",
    name: "fill-drip",
  },
  {
    icon: "fa-solid fa-fill fa-fw",
    name: "fill",
  },
  {
    icon: "fa-solid fa-file-zipper fa-fw",
    name: "file-zipper",
  },
  {
    icon: "fa-solid fa-file-waveform fa-fw",
    name: "file-waveform",
  },
  {
    icon: "fa-solid fa-file-video fa-fw",
    name: "file-video",
  },
  {
    icon: "fa-solid fa-file-signature fa-fw",
    name: "file-signature",
  },
  {
    icon: "fa-solid fa-file-shield fa-fw",
    name: "file-shield",
  },
  {
    icon: "fa-solid fa-file-prescription fa-fw",
    name: "file-prescription",
  },
  {
    icon: "fa-solid fa-file-powerpoint fa-fw",
    name: "file-powerpoint",
  },
  {
    icon: "fa-solid fa-file-pen fa-fw",
    name: "file-pen",
  },
  {
    icon: "fa-solid fa-file-medical fa-fw",
    name: "file-medical",
  },
  {
    icon: "fa-solid fa-file-lines fa-fw",
    name: "file-lines",
  },
  {
    icon: "fa-solid fa-file-invoice-dollar fa-fw",
    name: "file-invoice-dollar",
  },
  {
    icon: "fa-solid fa-file-image fa-fw",
    name: "file-image",
  },
  {
    icon: "fa-solid fa-file-csv fa-fw",
    name: "file-csv",
  },
  {
    icon: "fa-solid fa-file-code fa-fw",
    name: "file-code",
  },
  {
    icon: "fa-solid fa-file-circle-xmark fa-fw",
    name: "file-circle-xmark",
  },
  {
    icon: "fa-solid fa-file-circle-question fa-fw",
    name: "file-circle-question",
  },
  {
    icon: "fa-solid fa-file-circle-plus fa-fw",
    name: "file-circle-plus",
  },
  {
    icon: "fa-solid fa-file-circle-minus fa-fw",
    name: "file-circle-minus",
  },
  {
    icon: "fa-solid fa-file-circle-exclamation fa-fw",
    name: "file-circle-exclamation",
  },
  {
    icon: "fa-solid fa-file-circle-check fa-fw",
    name: "file-circle-check",
  },
  {
    icon: "fa-solid fa-file-audio fa-fw",
    name: "file-audio",
  },
  {
    icon: "fa-solid fa-file-arrow-up fa-fw",
    name: "file-arrow-up",
  },
  {
    icon: "fa-solid fa-file-arrow-down fa-fw",
    name: "file-arrow-down",
  },
  {
    icon: "fa-solid fa-ferry fa-fw",
    name: "ferry",
  },
  {
    icon: "fa-solid fa-feather-pointed fa-fw",
    name: "feather-pointed",
  },
  {
    icon: "fa-solid fa-fax fa-fw",
    name: "fax",
  },
  {
    icon: "fa-solid fa-faucet-drip fa-fw",
    name: "faucet-drip",
  },
  {
    icon: "fa-solid fa-faucet fa-fw",
    name: "faucet",
  },
  {
    icon: "fa-solid fa-fan fa-fw",
    name: "fan",
  },
  {
    icon: "fa-solid fa-face-tired fa-fw",
    name: "face-tired",
  },
  {
    icon: "fa-solid fa-face-surprise fa-fw",
    name: "face-surprise",
  },
  {
    icon: "fa-solid fa-face-smile-wink fa-fw",
    name: "face-smile-wink",
  },
  {
    icon: "fa-solid fa-face-smile-beam fa-fw",
    name: "face-smile-beam",
  },
  {
    icon: "fa-solid fa-face-sad-tear fa-fw",
    name: "face-sad-tear",
  },
  {
    icon: "fa-solid fa-face-sad-cry fa-fw",
    name: "face-sad-cry",
  },
  {
    icon: "fa-solid fa-face-rolling-eyes fa-fw",
    name: "face-rolling-eyes",
  },
  {
    icon: "fa-solid fa-face-meh-blank fa-fw",
    name: "face-meh-blank",
  },
  {
    icon: "fa-solid fa-face-meh fa-fw",
    name: "face-meh",
  },
  {
    icon: "fa-solid fa-face-laugh-wink fa-fw",
    name: "face-laugh-wink",
  },
  {
    icon: "fa-solid fa-face-laugh-squint fa-fw",
    name: "face-laugh-squint",
  },
  {
    icon: "fa-solid fa-face-laugh-beam fa-fw",
    name: "face-laugh-beam",
  },
  {
    icon: "fa-solid fa-face-laugh fa-fw",
    name: "face-laugh",
  },
  {
    icon: "fa-solid fa-face-kiss-wink-heart fa-fw",
    name: "face-kiss-wink-heart",
  },
  {
    icon: "fa-solid fa-face-kiss-beam fa-fw",
    name: "face-kiss-beam",
  },
  {
    icon: "fa-solid fa-face-kiss fa-fw",
    name: "face-kiss",
  },
  {
    icon: "fa-solid fa-face-grin-wink fa-fw",
    name: "face-grin-wink",
  },
  {
    icon: "fa-solid fa-face-grin-wide fa-fw",
    name: "face-grin-wide",
  },
  {
    icon: "fa-solid fa-face-grin-tongue-wink fa-fw",
    name: "face-grin-tongue-wink",
  },
  {
    icon: "fa-solid fa-face-grin-tongue-squint fa-fw",
    name: "face-grin-tongue-squint",
  },
  {
    icon: "fa-solid fa-face-grin-tongue fa-fw",
    name: "face-grin-tongue",
  },
  {
    icon: "fa-solid fa-face-grin-tears fa-fw",
    name: "face-grin-tears",
  },
  {
    icon: "fa-solid fa-face-grin-stars fa-fw",
    name: "face-grin-stars",
  },
  {
    icon: "fa-solid fa-face-grin-squint-tears fa-fw",
    name: "face-grin-squint-tears",
  },
  {
    icon: "fa-solid fa-face-grin-squint fa-fw",
    name: "face-grin-squint",
  },
  {
    icon: "fa-solid fa-face-grin-hearts fa-fw",
    name: "face-grin-hearts",
  },
  {
    icon: "fa-solid fa-face-grin-beam-sweat fa-fw",
    name: "face-grin-beam-sweat",
  },
  {
    icon: "fa-solid fa-face-grin-beam fa-fw",
    name: "face-grin-beam",
  },
  {
    icon: "fa-solid fa-face-grin fa-fw",
    name: "face-grin",
  },
  {
    icon: "fa-solid fa-face-grimace fa-fw",
    name: "face-grimace",
  },
  {
    icon: "fa-solid fa-face-frown-open fa-fw",
    name: "face-frown-open",
  },
  {
    icon: "fa-solid fa-face-frown fa-fw",
    name: "face-frown",
  },
  {
    icon: "fa-solid fa-face-flushed fa-fw",
    name: "face-flushed",
  },
  {
    icon: "fa-solid fa-face-dizzy fa-fw",
    name: "face-dizzy",
  },
  {
    icon: "fa-solid fa-face-angry fa-fw",
    name: "face-angry",
  },
  {
    icon: "fa-solid fa-f fa-fw",
    name: "f",
  },
  {
    icon: "fa-solid fa-eye-low-vision fa-fw",
    name: "eye-low-vision",
  },
  {
    icon: "fa-solid fa-eye-dropper fa-fw",
    name: "eye-dropper",
  },
  {
    icon: "fa-solid fa-explosion fa-fw",
    name: "explosion",
  },
  {
    icon: "fa-solid fa-euro-sign fa-fw",
    name: "euro-sign",
  },
  {
    icon: "fa-solid fa-ethernet fa-fw",
    name: "ethernet",
  },
  {
    icon: "fa-solid fa-equals fa-fw",
    name: "equals",
  },
  {
    icon: "fa-solid fa-envelopes-bulk fa-fw",
    name: "envelopes-bulk",
  },
  {
    icon: "fa-solid fa-envelope-open-text fa-fw",
    name: "envelope-open-text",
  },
  {
    icon: "fa-solid fa-envelope-open fa-fw",
    name: "envelope-open",
  },
  {
    icon: "fa-solid fa-envelope-circle-check fa-fw",
    name: "envelope-circle-check",
  },
  {
    icon: "fa-solid fa-ellipsis-vertical fa-fw",
    name: "ellipsis-vertical",
  },
  {
    icon: "fa-solid fa-ellipsis fa-fw",
    name: "ellipsis",
  },
  {
    icon: "fa-solid fa-elevator fa-fw",
    name: "elevator",
  },
  {
    icon: "fa-solid fa-eject fa-fw",
    name: "eject",
  },
  {
    icon: "fa-solid fa-egg fa-fw",
    name: "egg",
  },
  {
    icon: "fa-solid fa-earth-oceania fa-fw",
    name: "earth-oceania",
  },
  {
    icon: "fa-solid fa-earth-europe fa-fw",
    name: "earth-europe",
  },
  {
    icon: "fa-solid fa-earth-asia fa-fw",
    name: "earth-asia",
  },
  {
    icon: "fa-solid fa-earth-africa fa-fw",
    name: "earth-africa",
  },
  {
    icon: "fa-solid fa-ear-listen fa-fw",
    name: "ear-listen",
  },
  {
    icon: "fa-solid fa-ear-deaf fa-fw",
    name: "ear-deaf",
  },
  {
    icon: "fa-solid fa-e fa-fw",
    name: "e",
  },
  {
    icon: "fa-solid fa-dungeon fa-fw",
    name: "dungeon",
  },
  {
    icon: "fa-solid fa-dumpster fa-fw",
    name: "dumpster",
  },
  {
    icon: "fa-solid fa-drumstick-bite fa-fw",
    name: "drumstick-bite",
  },
  {
    icon: "fa-solid fa-drum-steelpan fa-fw",
    name: "drum-steelpan",
  },
  {
    icon: "fa-solid fa-drum fa-fw",
    name: "drum",
  },
  {
    icon: "fa-solid fa-droplet-slash fa-fw",
    name: "droplet-slash",
  },
  {
    icon: "fa-solid fa-draw-polygon fa-fw",
    name: "draw-polygon",
  },
  {
    icon: "fa-solid fa-down-long fa-fw",
    name: "down-long",
  },
  {
    icon: "fa-solid fa-down-left-and-up-right-to-center fa-fw",
    name: "down-left-and-up-right-to-center",
  },
  {
    icon: "fa-solid fa-dove fa-fw",
    name: "dove",
  },
  {
    icon: "fa-solid fa-door-closed fa-fw",
    name: "door-closed",
  },
  {
    icon: "fa-solid fa-dong-sign fa-fw",
    name: "dong-sign",
  },
  {
    icon: "fa-solid fa-dolly fa-fw",
    name: "dolly",
  },
  {
    icon: "fa-solid fa-dog fa-fw",
    name: "dog",
  },
  {
    icon: "fa-solid fa-dna fa-fw",
    name: "dna",
  },
  {
    icon: "fa-solid fa-divide fa-fw",
    name: "divide",
  },
  {
    icon: "fa-solid fa-display fa-fw",
    name: "display",
  },
  {
    icon: "fa-solid fa-disease fa-fw",
    name: "disease",
  },
  {
    icon: "fa-solid fa-dice-two fa-fw",
    name: "dice-two",
  },
  {
    icon: "fa-solid fa-dice-three fa-fw",
    name: "dice-three",
  },
  {
    icon: "fa-solid fa-dice-six fa-fw",
    name: "dice-six",
  },
  {
    icon: "fa-solid fa-dice-one fa-fw",
    name: "dice-one",
  },
  {
    icon: "fa-solid fa-dice-four fa-fw",
    name: "dice-four",
  },
  {
    icon: "fa-solid fa-dice-five fa-fw",
    name: "dice-five",
  },
  {
    icon: "fa-solid fa-dice-d6 fa-fw",
    name: "dice-d6",
  },
  {
    icon: "fa-solid fa-dice-d20 fa-fw",
    name: "dice-d20",
  },
  {
    icon: "fa-solid fa-diamond-turn-right fa-fw",
    name: "diamond-turn-right",
  },
  {
    icon: "fa-solid fa-diagram-successor fa-fw",
    name: "diagram-successor",
  },
  {
    icon: "fa-solid fa-diagram-project fa-fw",
    name: "diagram-project",
  },
  {
    icon: "fa-solid fa-diagram-predecessor fa-fw",
    name: "diagram-predecessor",
  },
  {
    icon: "fa-solid fa-diagram-next fa-fw",
    name: "diagram-next",
  },
  {
    icon: "fa-solid fa-dharmachakra fa-fw",
    name: "dharmachakra",
  },
  {
    icon: "fa-solid fa-democrat fa-fw",
    name: "democrat",
  },
  {
    icon: "fa-solid fa-delete-left fa-fw",
    name: "delete-left",
  },
  {
    icon: "fa-solid fa-d fa-fw",
    name: "d",
  },
  {
    icon: "fa-solid fa-cubes-stacked fa-fw",
    name: "cubes-stacked",
  },
  {
    icon: "fa-solid fa-cubes fa-fw",
    name: "cubes",
  },
  {
    icon: "fa-solid fa-cruzeiro-sign fa-fw",
    name: "cruzeiro-sign",
  },
  {
    icon: "fa-solid fa-crutch fa-fw",
    name: "crutch",
  },
  {
    icon: "fa-solid fa-crow fa-fw",
    name: "crow",
  },
  {
    icon: "fa-solid fa-crop-simple fa-fw",
    name: "crop-simple",
  },
  {
    icon: "fa-solid fa-crop fa-fw",
    name: "crop",
  },
  {
    icon: "fa-solid fa-cow fa-fw",
    name: "cow",
  },
  {
    icon: "fa-solid fa-couch fa-fw",
    name: "couch",
  },
  {
    icon: "fa-solid fa-cookie fa-fw",
    name: "cookie",
  },
  {
    icon: "fa-solid fa-computer-mouse fa-fw",
    name: "computer-mouse",
  },
  {
    icon: "fa-solid fa-computer fa-fw",
    name: "computer",
  },
  {
    icon: "fa-solid fa-compress fa-fw",
    name: "compress",
  },
  {
    icon: "fa-solid fa-compass-drafting fa-fw",
    name: "compass-drafting",
  },
  {
    icon: "fa-solid fa-compact-disc fa-fw",
    name: "compact-disc",
  },
  {
    icon: "fa-solid fa-comment-sms fa-fw",
    name: "comment-sms",
  },
  {
    icon: "fa-solid fa-comment-slash fa-fw",
    name: "comment-slash",
  },
  {
    icon: "fa-solid fa-comment-medical fa-fw",
    name: "comment-medical",
  },
  {
    icon: "fa-solid fa-comment-dots fa-fw",
    name: "comment-dots",
  },
  {
    icon: "fa-solid fa-comment-dollar fa-fw",
    name: "comment-dollar",
  },
  {
    icon: "fa-solid fa-colon-sign fa-fw",
    name: "colon-sign",
  },
  {
    icon: "fa-solid fa-code-pull-request fa-fw",
    name: "code-pull-request",
  },
  {
    icon: "fa-solid fa-code-merge fa-fw",
    name: "code-merge",
  },
  {
    icon: "fa-solid fa-code-fork fa-fw",
    name: "code-fork",
  },
  {
    icon: "fa-solid fa-code-commit fa-fw",
    name: "code-commit",
  },
  {
    icon: "fa-solid fa-clover fa-fw",
    name: "clover",
  },
  {
    icon: "fa-solid fa-cloud-sun-rain fa-fw",
    name: "cloud-sun-rain",
  },
  {
    icon: "fa-solid fa-cloud-sun fa-fw",
    name: "cloud-sun",
  },
  {
    icon: "fa-solid fa-cloud-showers-water fa-fw",
    name: "cloud-showers-water",
  },
  {
    icon: "fa-solid fa-cloud-showers-heavy fa-fw",
    name: "cloud-showers-heavy",
  },
  {
    icon: "fa-solid fa-cloud-rain fa-fw",
    name: "cloud-rain",
  },
  {
    icon: "fa-solid fa-cloud-moon-rain fa-fw",
    name: "cloud-moon-rain",
  },
  {
    icon: "fa-solid fa-cloud-moon fa-fw",
    name: "cloud-moon",
  },
  {
    icon: "fa-solid fa-cloud-meatball fa-fw",
    name: "cloud-meatball",
  },
  {
    icon: "fa-solid fa-cloud-bolt fa-fw",
    name: "cloud-bolt",
  },
  {
    icon: "fa-solid fa-cloud-arrow-down fa-fw",
    name: "cloud-arrow-down",
  },
  {
    icon: "fa-solid fa-clock-rotate-left fa-fw",
    name: "clock-rotate-left",
  },
  {
    icon: "fa-solid fa-clipboard-user fa-fw",
    name: "clipboard-user",
  },
  {
    icon: "fa-solid fa-clipboard-question fa-fw",
    name: "clipboard-question",
  },
  {
    icon: "fa-solid fa-clipboard-list fa-fw",
    name: "clipboard-list",
  },
  {
    icon: "fa-solid fa-clipboard-check fa-fw",
    name: "clipboard-check",
  },
  {
    icon: "fa-solid fa-clapperboard fa-fw",
    name: "clapperboard",
  },
  {
    icon: "fa-solid fa-circle-stop fa-fw",
    name: "circle-stop",
  },
  {
    icon: "fa-solid fa-circle-right fa-fw",
    name: "circle-right",
  },
  {
    icon: "fa-solid fa-circle-radiation fa-fw",
    name: "circle-radiation",
  },
  {
    icon: "fa-solid fa-circle-question fa-fw",
    name: "circle-question",
  },
  {
    icon: "fa-solid fa-circle-plus fa-fw",
    name: "circle-plus",
  },
  {
    icon: "fa-solid fa-circle-play fa-fw",
    name: "circle-play",
  },
  {
    icon: "fa-solid fa-circle-pause fa-fw",
    name: "circle-pause",
  },
  {
    icon: "fa-solid fa-circle-nodes fa-fw",
    name: "circle-nodes",
  },
  {
    icon: "fa-solid fa-circle-minus fa-fw",
    name: "circle-minus",
  },
  {
    icon: "fa-solid fa-circle-left fa-fw",
    name: "circle-left",
  },
  {
    icon: "fa-solid fa-circle-h fa-fw",
    name: "circle-h",
  },
  {
    icon: "fa-solid fa-circle-dot fa-fw",
    name: "circle-dot",
  },
  {
    icon: "fa-solid fa-circle-dollar-to-slot fa-fw",
    name: "circle-dollar-to-slot",
  },
  {
    icon: "fa-solid fa-circle-chevron-up fa-fw",
    name: "circle-chevron-up",
  },
  {
    icon: "fa-solid fa-circle-chevron-right fa-fw",
    name: "circle-chevron-right",
  },
  {
    icon: "fa-solid fa-circle-chevron-left fa-fw",
    name: "circle-chevron-left",
  },
  {
    icon: "fa-solid fa-circle-chevron-down fa-fw",
    name: "circle-chevron-down",
  },
  {
    icon: "fa-solid fa-circle-arrow-up fa-fw",
    name: "circle-arrow-up",
  },
  {
    icon: "fa-solid fa-circle-arrow-right fa-fw",
    name: "circle-arrow-right",
  },
  {
    icon: "fa-solid fa-circle-arrow-left fa-fw",
    name: "circle-arrow-left",
  },
  {
    icon: "fa-solid fa-circle-arrow-down fa-fw",
    name: "circle-arrow-down",
  },
  {
    icon: "fa-solid fa-children fa-fw",
    name: "children",
  },
  {
    icon: "fa-solid fa-child-rifle fa-fw",
    name: "child-rifle",
  },
  {
    icon: "fa-solid fa-child-reaching fa-fw",
    name: "child-reaching",
  },
  {
    icon: "fa-solid fa-child-dress fa-fw",
    name: "child-dress",
  },
  {
    icon: "fa-solid fa-chevron-right fa-fw",
    name: "chevron-right",
  },
  {
    icon: "fa-solid fa-chevron-left fa-fw",
    name: "chevron-left",
  },
  {
    icon: "fa-solid fa-chess-rook fa-fw",
    name: "chess-rook",
  },
  {
    icon: "fa-solid fa-chess-queen fa-fw",
    name: "chess-queen",
  },
  {
    icon: "fa-solid fa-chess-pawn fa-fw",
    name: "chess-pawn",
  },
  {
    icon: "fa-solid fa-chess-knight fa-fw",
    name: "chess-knight",
  },
  {
    icon: "fa-solid fa-chess-king fa-fw",
    name: "chess-king",
  },
  {
    icon: "fa-solid fa-chess-board fa-fw",
    name: "chess-board",
  },
  {
    icon: "fa-solid fa-chess-bishop fa-fw",
    name: "chess-bishop",
  },
  {
    icon: "fa-solid fa-chess fa-fw",
    name: "chess",
  },
  {
    icon: "fa-solid fa-cheese fa-fw",
    name: "cheese",
  },
  {
    icon: "fa-solid fa-check-to-slot fa-fw",
    name: "check-to-slot",
  },
  {
    icon: "fa-solid fa-check-double fa-fw",
    name: "check-double",
  },
  {
    icon: "fa-solid fa-chart-pie fa-fw",
    name: "chart-pie",
  },
  {
    icon: "fa-solid fa-chart-line fa-fw",
    name: "chart-line",
  },
  {
    icon: "fa-solid fa-chart-gantt fa-fw",
    name: "chart-gantt",
  },
  {
    icon: "fa-solid fa-chart-column fa-fw",
    name: "chart-column",
  },
  {
    icon: "fa-solid fa-chart-bar fa-fw",
    name: "chart-bar",
  },
  {
    icon: "fa-solid fa-chart-area fa-fw",
    name: "chart-area",
  },
  {
    icon: "fa-solid fa-charging-station fa-fw",
    name: "charging-station",
  },
  {
    icon: "fa-solid fa-champagne-glasses fa-fw",
    name: "champagne-glasses",
  },
  {
    icon: "fa-solid fa-chalkboard-user fa-fw",
    name: "chalkboard-user",
  },
  {
    icon: "fa-solid fa-cent-sign fa-fw",
    name: "cent-sign",
  },
  {
    icon: "fa-solid fa-cedi-sign fa-fw",
    name: "cedi-sign",
  },
  {
    icon: "fa-solid fa-cat fa-fw",
    name: "cat",
  },
  {
    icon: "fa-solid fa-cart-flatbed-suitcase fa-fw",
    name: "cart-flatbed-suitcase",
  },
  {
    icon: "fa-solid fa-cart-flatbed fa-fw",
    name: "cart-flatbed",
  },
  {
    icon: "fa-solid fa-cart-arrow-down fa-fw",
    name: "cart-arrow-down",
  },
  {
    icon: "fa-solid fa-carrot fa-fw",
    name: "carrot",
  },
  {
    icon: "fa-solid fa-caret-right fa-fw",
    name: "caret-right",
  },
  {
    icon: "fa-solid fa-caret-left fa-fw",
    name: "caret-left",
  },
  {
    icon: "fa-solid fa-caravan fa-fw",
    name: "caravan",
  },
  {
    icon: "fa-solid fa-car-tunnel fa-fw",
    name: "car-tunnel",
  },
  {
    icon: "fa-solid fa-car-rear fa-fw",
    name: "car-rear",
  },
  {
    icon: "fa-solid fa-car-on fa-fw",
    name: "car-on",
  },
  {
    icon: "fa-solid fa-car-burst fa-fw",
    name: "car-burst",
  },
  {
    icon: "fa-solid fa-car-battery fa-fw",
    name: "car-battery",
  },
  {
    icon: "fa-solid fa-capsules fa-fw",
    name: "capsules",
  },
  {
    icon: "fa-solid fa-cannabis fa-fw",
    name: "cannabis",
  },
  {
    icon: "fa-solid fa-candy-cane fa-fw",
    name: "candy-cane",
  },
  {
    icon: "fa-solid fa-campground fa-fw",
    name: "campground",
  },
  {
    icon: "fa-solid fa-camera-rotate fa-fw",
    name: "camera-rotate",
  },
  {
    icon: "fa-solid fa-calendar-xmark fa-fw",
    name: "calendar-xmark",
  },
  {
    icon: "fa-solid fa-calendar-plus fa-fw",
    name: "calendar-plus",
  },
  {
    icon: "fa-solid fa-calendar-minus fa-fw",
    name: "calendar-minus",
  },
  {
    icon: "fa-solid fa-calendar-day fa-fw",
    name: "calendar-day",
  },
  {
    icon: "fa-solid fa-calendar-check fa-fw",
    name: "calendar-check",
  },
  {
    icon: "fa-solid fa-cake-candles fa-fw",
    name: "cake-candles",
  },
  {
    icon: "fa-solid fa-c fa-fw",
    name: "c",
  },
  {
    icon: "fa-solid fa-bus-simple fa-fw",
    name: "bus-simple",
  },
  {
    icon: "fa-solid fa-bus fa-fw",
    name: "bus",
  },
  {
    icon: "fa-solid fa-burst fa-fw",
    name: "burst",
  },
  {
    icon: "fa-solid fa-burger fa-fw",
    name: "burger",
  },
  {
    icon: "fa-solid fa-bullhorn fa-fw",
    name: "bullhorn",
  },
  {
    icon: "fa-solid fa-building-wheat fa-fw",
    name: "building-wheat",
  },
  {
    icon: "fa-solid fa-building-user fa-fw",
    name: "building-user",
  },
  {
    icon: "fa-solid fa-building-un fa-fw",
    name: "building-un",
  },
  {
    icon: "fa-solid fa-building-shield fa-fw",
    name: "building-shield",
  },
  {
    icon: "fa-solid fa-building-ngo fa-fw",
    name: "building-ngo",
  },
  {
    icon: "fa-solid fa-building-lock fa-fw",
    name: "building-lock",
  },
  {
    icon: "fa-solid fa-building-flag fa-fw",
    name: "building-flag",
  },
  {
    icon: "fa-solid fa-building-columns fa-fw",
    name: "building-columns",
  },
  {
    icon: "fa-solid fa-building-circle-xmark fa-fw",
    name: "building-circle-xmark",
  },
  {
    icon: "fa-solid fa-building-circle-exclamation fa-fw",
    name: "building-circle-exclamation",
  },
  {
    icon: "fa-solid fa-building-circle-check fa-fw",
    name: "building-circle-check",
  },
  {
    icon: "fa-solid fa-building-circle-arrow-right fa-fw",
    name: "building-circle-arrow-right",
  },
  {
    icon: "fa-solid fa-bugs fa-fw",
    name: "bugs",
  },
  {
    icon: "fa-solid fa-bug-slash fa-fw",
    name: "bug-slash",
  },
  {
    icon: "fa-solid fa-bucket fa-fw",
    name: "bucket",
  },
  {
    icon: "fa-solid fa-broom-ball fa-fw",
    name: "broom-ball",
  },
  {
    icon: "fa-solid fa-broom fa-fw",
    name: "broom",
  },
  {
    icon: "fa-solid fa-briefcase-medical fa-fw",
    name: "briefcase-medical",
  },
  {
    icon: "fa-solid fa-bread-slice fa-fw",
    name: "bread-slice",
  },
  {
    icon: "fa-solid fa-brazilian-real-sign fa-fw",
    name: "brazilian-real-sign",
  },
  {
    icon: "fa-solid fa-braille fa-fw",
    name: "braille",
  },
  {
    icon: "fa-solid fa-boxes-stacked fa-fw",
    name: "boxes-stacked",
  },
  {
    icon: "fa-solid fa-boxes-packing fa-fw",
    name: "boxes-packing",
  },
  {
    icon: "fa-solid fa-box-tissue fa-fw",
    name: "box-tissue",
  },
  {
    icon: "fa-solid fa-box-open fa-fw",
    name: "box-open",
  },
  {
    icon: "fa-solid fa-box-archive fa-fw",
    name: "box-archive",
  },
  {
    icon: "fa-solid fa-box fa-fw",
    name: "box",
  },
  {
    icon: "fa-solid fa-bowling-ball fa-fw",
    name: "bowling-ball",
  },
  {
    icon: "fa-solid fa-bowl-rice fa-fw",
    name: "bowl-rice",
  },
  {
    icon: "fa-solid fa-bowl-food fa-fw",
    name: "bowl-food",
  },
  {
    icon: "fa-solid fa-bottle-water fa-fw",
    name: "bottle-water",
  },
  {
    icon: "fa-solid fa-bottle-droplet fa-fw",
    name: "bottle-droplet",
  },
  {
    icon: "fa-solid fa-bore-hole fa-fw",
    name: "bore-hole",
  },
  {
    icon: "fa-solid fa-book-tanakh fa-fw",
    name: "book-tanakh",
  },
  {
    icon: "fa-solid fa-book-quran fa-fw",
    name: "book-quran",
  },
  {
    icon: "fa-solid fa-book-open-reader fa-fw",
    name: "book-open-reader",
  },
  {
    icon: "fa-solid fa-book-open fa-fw",
    name: "book-open",
  },
  {
    icon: "fa-solid fa-book-medical fa-fw",
    name: "book-medical",
  },
  {
    icon: "fa-solid fa-book-journal-whills fa-fw",
    name: "book-journal-whills",
  },
  {
    icon: "fa-solid fa-book-bookmark fa-fw",
    name: "book-bookmark",
  },
  {
    icon: "fa-solid fa-book-bible fa-fw",
    name: "book-bible",
  },
  {
    icon: "fa-solid fa-book-atlas fa-fw",
    name: "book-atlas",
  },
  {
    icon: "fa-solid fa-bong fa-fw",
    name: "bong",
  },
  {
    icon: "fa-solid fa-bone fa-fw",
    name: "bone",
  },
  {
    icon: "fa-solid fa-bolt-lightning fa-fw",
    name: "bolt-lightning",
  },
  {
    icon: "fa-solid fa-bold fa-fw",
    name: "bold",
  },
  {
    icon: "fa-solid fa-blender-phone fa-fw",
    name: "blender-phone",
  },
  {
    icon: "fa-solid fa-blender fa-fw",
    name: "blender",
  },
  {
    icon: "fa-solid fa-bitcoin-sign fa-fw",
    name: "bitcoin-sign",
  },
  {
    icon: "fa-solid fa-biohazard fa-fw",
    name: "biohazard",
  },
  {
    icon: "fa-solid fa-bezier-curve fa-fw",
    name: "bezier-curve",
  },
  {
    icon: "fa-solid fa-bell-slash fa-fw",
    name: "bell-slash",
  },
  {
    icon: "fa-solid fa-bell-concierge fa-fw",
    name: "bell-concierge",
  },
  {
    icon: "fa-solid fa-beer-mug-empty fa-fw",
    name: "beer-mug-empty",
  },
  {
    icon: "fa-solid fa-bed-pulse fa-fw",
    name: "bed-pulse",
  },
  {
    icon: "fa-solid fa-bed fa-fw",
    name: "bed",
  },
  {
    icon: "fa-solid fa-basketball fa-fw",
    name: "basketball",
  },
  {
    icon: "fa-solid fa-bars-staggered fa-fw",
    name: "bars-staggered",
  },
  {
    icon: "fa-solid fa-bars-progress fa-fw",
    name: "bars-progress",
  },
  {
    icon: "fa-solid fa-bandage fa-fw",
    name: "bandage",
  },
  {
    icon: "fa-solid fa-ban-smoking fa-fw",
    name: "ban-smoking",
  },
  {
    icon: "fa-solid fa-ban fa-fw",
    name: "ban",
  },
  {
    icon: "fa-solid fa-baht-sign fa-fw",
    name: "baht-sign",
  },
  {
    icon: "fa-solid fa-bahai fa-fw",
    name: "bahai",
  },
  {
    icon: "fa-solid fa-bacterium fa-fw",
    name: "bacterium",
  },
  {
    icon: "fa-solid fa-bacteria fa-fw",
    name: "bacteria",
  },
  {
    icon: "fa-solid fa-bacon fa-fw",
    name: "bacon",
  },
  {
    icon: "fa-solid fa-backward-step fa-fw",
    name: "backward-step",
  },
  {
    icon: "fa-solid fa-backward-fast fa-fw",
    name: "backward-fast",
  },
  {
    icon: "fa-solid fa-baby-carriage fa-fw",
    name: "baby-carriage",
  },
  {
    icon: "fa-solid fa-b fa-fw",
    name: "b",
  },
  {
    icon: "fa-solid fa-austral-sign fa-fw",
    name: "austral-sign",
  },
  {
    icon: "fa-solid fa-atom fa-fw",
    name: "atom",
  },
  {
    icon: "fa-solid fa-at fa-fw",
    name: "at",
  },
  {
    icon: "fa-solid fa-asterisk fa-fw",
    name: "asterisk",
  },
  {
    icon: "fa-solid fa-archway fa-fw",
    name: "archway",
  },
  {
    icon: "fa-solid fa-apple-whole fa-fw",
    name: "apple-whole",
  },
  {
    icon: "fa-solid fa-ankh fa-fw",
    name: "ankh",
  },
  {
    icon: "fa-solid fa-anchor-lock fa-fw",
    name: "anchor-lock",
  },
  {
    icon: "fa-solid fa-anchor-circle-xmark fa-fw",
    name: "anchor-circle-xmark",
  },
  {
    icon: "fa-solid fa-anchor-circle-exclamation fa-fw",
    name: "anchor-circle-exclamation",
  },
  {
    icon: "fa-solid fa-anchor-circle-check fa-fw",
    name: "anchor-circle-check",
  },


];
iconosFontAwesome.sort((a, b) => a.name.localeCompare(b.name));
iconosFontAwesome.filter((item) => item.icon.includes("fa-solid"));

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
