




function togglePasswordVisibility(passwordSelector, iconSelector) {
    const $passwordInput = $(passwordSelector);
    const $toggleIcon = $(iconSelector);


    // Mostrar ícono si hay texto
    $passwordInput.on('input', function () {
      if ($(this).val().length > 0) {
        $toggleIcon.show();
      } else {
        $toggleIcon.hide();
        $passwordInput.attr('type', 'password');
        $toggleIcon.removeClass('fa-eye-slash').addClass('fa-eye');
      }
    });

    // Alternar visibilidad de la contraseña
    $toggleIcon.on('click', function () {
      const type = $passwordInput.attr('type') === 'password' ? 'text' : 'password';
      $passwordInput.attr('type', type);
      $(this).toggleClass('fa-eye fa-eye-slash');
    });

    if ($passwordInput.val().length === 0) {
      $toggleIcon.hide();
    }
  }

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



console.log("common.js cargado (versión con jQuery para UI).");