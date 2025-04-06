document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const menuLinks = document.querySelectorAll('#sidebar .menu-link'); // Solo enlaces que cargan contenido
    const currentActive = document.querySelector('#sidebar .active-link'); // Si ya hay uno activo al cargar

    // 1. Toggle Sidebar
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            // Podrías necesitar ajustar el ancho del content aquí si no usas flexbox de forma adecuada
            // document.getElementById('content').classList.toggle('active');
        });
    }

    // 2. Marcar enlace activo y guardar en localStorage
    const setActiveLink = (linkElement) => {
        // Remover clase activa de cualquier otro enlace
        menuLinks.forEach(link => link.classList.remove('active-link'));
        if(linkElement) {
            linkElement.classList.add('active-link');
            // Guardar la URL del enlace activo
            localStorage.setItem('activeMenuLink', linkElement.getAttribute('href'));

            // Abrir menús padre si están colapsados (opcional pero útil)
            let parentCollapse = linkElement.closest('.collapse');
            while(parentCollapse) {
                let collapseInstance = new bootstrap.Collapse(parentCollapse, {
                    toggle: false // Evita cerrar si ya está abierto
                });
                collapseInstance.show();
                 // Buscar el siguiente nivel padre
                parentCollapse = parentCollapse.parentElement.closest('.collapse');
            }
        } else {
             localStorage.removeItem('activeMenuLink');
        }
    };

    // Añadir event listeners a los enlaces del menú
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // No prevenir default si es un enlace real de iframe
            // e.preventDefault(); // Quitado para que funcione el target="main-iframe"

            setActiveLink(this);

            // Opcional: Si la pantalla es pequeña, cerrar el sidebar después de hacer clic
            if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
                 sidebar.classList.remove('active');
            }
        });
    });

     // 3. Restaurar el enlace activo al cargar la página
    const activeLinkHref = localStorage.getItem('activeMenuLink');
    if (activeLinkHref) {
        const linkToActivate = document.querySelector(`#sidebar a[href="${activeLinkHref}"]`);
        if (linkToActivate && linkToActivate.classList.contains('menu-link')) { // Asegura que es un enlace de contenido
            setActiveLink(linkToActivate);
            // Asegurarse de que el iframe muestre el contenido correcto al recargar
            document.getElementById('main-iframe').src = activeLinkHref;
        }
    } else {
        // Si no hay nada guardado, activa el primer enlace (Dashboard) si existe
        const dashboardLink = document.querySelector('#sidebar a[href="dashboard_content.html"]');
        if (dashboardLink) {
             setActiveLink(dashboardLink);
        }
    }


    // 4. Manejar el clic en Logout (ejemplo)
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault(); // Previene la navegación si href="#"
            if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
                // Aquí iría la lógica real de cierre de sesión
                console.log('Cerrando sesión...');
                // Por ejemplo, redirigir a la página de login
                // window.location.href = '/login.html';
                 alert('Sesión cerrada (simulación)');
                 localStorage.removeItem('activeMenuLink'); // Limpiar estado activo
            }
        });
    }

    // 5. Asegurarse que los dropdown-toggle no cambien el estado activo principal
    const dropdownToggles = document.querySelectorAll('#sidebar a.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            // Podrías añadir lógica aquí si necesitas que el menú padre se marque de alguna forma
            // pero sin quitar la clase 'active-link' del hijo que esté realmente activo.
        });
    });


});