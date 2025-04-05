document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificar autenticación al cargar la página
    redirectToLoginIfUnauthenticated();

    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const menuList = document.getElementById('menu-list');
    const mainIframe = document.getElementById('main-iframe');
    const logoutButton = document.getElementById('logout-button');
    const userGreeting = document.getElementById('user-greeting');
    const currentPageTitle = document.getElementById('current-page-title'); // Para mostrar título

    // --- Funciones del Sidebar y Menú ---

    // Función para mostrar/ocultar el sidebar
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            // Podrías guardar el estado en localStorage si quieres que persista
            // localStorage.setItem('sidebarActive', sidebar.classList.contains('active'));
        });
        // Recuperar estado del sidebar si se guardó
        // if (localStorage.getItem('sidebarActive') === 'true') {
        //    sidebar.classList.add('active');
        // }
    }

    // Función recursiva para construir el árbol del menú HTML
    function buildMenuTree(items, parentElement, level = 0) {
        const parentIdMap = items.reduce((map, item) => {
            const parentId = item.padre_id || 0; // Usa 0 para items raíz
            if (!map[parentId]) {
                map[parentId] = [];
            }
            map[parentId].push(item);
            return map;
        }, {});

        function renderLevel(parentId, container) {
            const children = (parentIdMap[parentId] || []).sort((a, b) => (a.orden || 0) - (b.orden || 0));

            children.forEach(item => {
                if (item.estado !== 0) return; // Omitir items deshabilitados

                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = '#'; // Usamos JS para la navegación
                a.dataset.tipo = item.tipo;
                a.dataset.valor = item.valor;
                a.dataset.nombre = item.nombre; // Guardar nombre para título

                let iconHtml = '';
                if (item.icono) {
                    // Asume que item.icono es una clase de Font Awesome como 'fas fa-home'
                    iconHtml = `<i class="${item.icono} fa-fw"></i> `;
                }

                a.innerHTML = `${iconHtml}${item.nombre}`;

                const subItems = parentIdMap[item.id];
                if (subItems && subItems.length > 0) {
                    // Es un nodo padre con hijos
                    a.classList.add('dropdown-toggle');
                    a.setAttribute('data-bs-toggle', 'collapse'); // Bootstrap 5 collapse
                    a.setAttribute('href', `#submenu-${item.id}`); // Apunta al ID del submenú
                    a.setAttribute('role', 'button');
                    a.setAttribute('aria-expanded', 'false'); // Inicia colapsado

                    const ulSubmenu = document.createElement('ul');
                    ulSubmenu.classList.add('collapse', 'list-unstyled', 'submenu');
                    ulSubmenu.id = `submenu-${item.id}`;

                    renderLevel(item.id, ulSubmenu); // Llamada recursiva para hijos

                    li.appendChild(a);
                    li.appendChild(ulSubmenu);
                } else {
                    // Es un nodo hoja (sin hijos)
                    li.appendChild(a);
                     // Añade listener solo a los elementos hoja que cargan contenido
                    a.addEventListener('click', handleMenuItemClick);
                }
                container.appendChild(li);
            });
        }
         // Inicia el renderizado desde los items raíz (padre_id 0 o null)
        renderLevel(0, parentElement);
    }


    // Manejador de clic para items del menú (hojas)
    function handleMenuItemClick(event) {
        event.preventDefault();
        const target = event.currentTarget; // El elemento <a> que fue clickeado
        const tipo = target.dataset.tipo;
        const valor = target.dataset.valor;
        const nombre = target.dataset.nombre || 'Página'; // Nombre para el título

        console.log(`Menú clickeado: Tipo=${tipo}, Valor=${valor}, Nombre=${nombre}`);

        // Remover clase activa de otros items (opcional, para estilo)
         document.querySelectorAll('#menu-list li.active').forEach(li => li.classList.remove('active'));
        // Añadir clase activa al li padre del item clickeado
         let parentLi = target.closest('li');
         if(parentLi) parentLi.classList.add('active');

        // Actualizar título de la página (opcional)
        if (currentPageTitle) {
            currentPageTitle.textContent = nombre;
        }


        if (tipo === 'iframe') {
            if (mainIframe) {
                 // Asegura que la URL sea relativa al dominio si no empieza con http
                const iframeSrc = valor.startsWith('http') ? valor : `/${valor.startsWith('/') ? valor.substring(1) : valor}`; // Ajusta la ruta base si es necesario
                console.log(`Cargando iframe: ${iframeSrc}`);
                mainIframe.src = iframeSrc;
            } else {
                console.error("Elemento iframe 'main-iframe' no encontrado.");
            }
        } else if (tipo === 'url') {
            // Abre en nueva pestaña si es URL externa, o navega si es interna (decide tu lógica)
            if (valor.startsWith('http://') || valor.startsWith('https://')) {
                console.log(`Abriendo URL externa: ${valor}`);
                window.open(valor, '_blank'); // Abre en nueva pestaña
            } else {
                // Asume URL interna relativa, carga en el iframe o navega la página completa
                console.log(`Navegando a URL interna (iframe): ${valor}`);
                 if (mainIframe) {
                      mainIframe.src = valor; // Carga URL interna en el iframe también
                 } else {
                      // O podrías navegar toda la página: window.location.href = valor;
                 }
            }
        } else if (tipo === 'formulario') {
             console.warn(`Tipo 'formulario' (${valor}) no implementado aún.`);
             // Aquí podrías cargar dinámicamente un formulario,
             // navegar a una página específica de formulario, etc.
              if (mainIframe) {
                 mainIframe.src = `/iframes/forms/${valor}.html`; // Ejemplo de carga de form en iframe
              }
        } else {
            console.warn(`Tipo de menú desconocido: ${tipo}`);
        }

         // Si el sidebar está activo (oculto en móviles), ocúltalo al hacer clic en un item
         if (window.innerWidth < 768 && sidebar.classList.contains('active')) {
             // sidebar.classList.remove('active'); // O usa el botón de toggle si existe
             if(sidebarCollapse) sidebarCollapse.click();
         }
    }

    // --- Carga de Datos Iniciales ---

    // Función para cargar datos del usuario y menú
    async function loadInitialData() {
        try {
             // 1. Obtener datos del usuario actual
             console.log("Obteniendo datos del usuario...");
             const userResponse = await fetchWithAuth('/api/v1/auth/users/me');
             if (!userResponse.ok) {
                 throw new Error(`Error ${userResponse.status} al obtener datos del usuario`);
             }
             const userData = await userResponse.json();
             console.log("Datos del usuario:", userData);
             if (userGreeting && userData.nombre_usuario) {
                 userGreeting.textContent = `Hola, ${userData.nombre_usuario}`;
             }

             // 2. Obtener menú (asume endpoint que devuelve menú para el usuario/empresa)
             //    Necesitarás crear este endpoint en tu API.
             //    Ej: /api/v1/menu/usuario/
             //    Este endpoint debería devolver solo los items de menú a los que el usuario tiene acceso
             //    basado en su empresa (y quizás roles).
             console.log("Obteniendo menú...");
             // Reemplaza '/api/v1/menu/usuario/' por tu endpoint real
             const menuResponse = await fetchWithAuth('/api/v1/menu/usuario/');
             if (!menuResponse.ok) {
                 throw new Error(`Error ${menuResponse.status} al obtener el menú`);
             }
             const menuData = await menuResponse.json();
             console.log("Datos del menú:", menuData);

             // 3. Construir el menú HTML
             menuList.innerHTML = ''; // Limpiar mensaje de carga/menú anterior
             if (menuData && menuData.length > 0) {
                 buildMenuTree(menuData, menuList);
             } else {
                 menuList.innerHTML = '<li><a>No hay opciones de menú disponibles.</a></li>';
             }

        } catch (error) {
            console.error("Error al cargar datos iniciales:", error);
             if (error.message !== 'Unauthorized') { // No mostrar error si ya fue manejado por fetchWithAuth
                showError(`Error cargando datos: ${error.message}`, 'error-message'); // Usa un div de error si existe
                // Podrías mostrar el error en el área del menú también
                if (menuList) menuList.innerHTML = '<li><a>Error al cargar menú.</a></li>';
             }
        } finally {
             // Ocultar cualquier indicador de carga general si lo hubiera
        }
    }


    // --- Event Listeners ---

    // Listener para el botón de logout
    if (logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault();
            console.log("Cerrando sesión...");
            removeToken(); // Elimina el token
            window.location.href = '/index.html'; // Redirige a la página de login
        });
    }

    // Cargar los datos iniciales al iniciar
    loadInitialData();

});