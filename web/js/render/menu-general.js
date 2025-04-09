let currentData = [];
let editModal;

document.addEventListener("DOMContentLoaded", () => {
    fetchMenus();
    editModal = new bootstrap.Modal(document.getElementById('editModal'));
    document.getElementById("editForm").addEventListener("submit", guardarCambios);
});

function fetchMenus() {
    fetch("/menu")
        .then(res => res.json())
        .then(data => {
            currentData = data;
            llenarTabla();
        });
}

function llenarTabla() {
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = "";
    currentData.forEach(menu => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${menu.nombre}</td>
            <td>${menu.icono}</td>
            <td>${menu.ruta ?? ""}</td>
            <td>${menu.tipo}</td>
            <td>${menu.orden}</td>
            <td>${menu.estado ? "Activo" : "Inactivo"}</td>
            <td><button class="btn btn-sm btn-warning" onclick="editar(${menu.id})">Editar</button></td>
        `;
        tbody.appendChild(row);
    });
}

function editar(id) {
    const menu = currentData.find(m => m.id === id);
    if (!menu) return;

    const form = document.getElementById("editForm");
    for (let key in menu) {
        if (form[key] !== undefined) {
            form[key].value = menu[key];
        }
    }
    editModal.show();
}

function guardarCambios(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    data.id = parseInt(data.id);
    data.orden = parseInt(data.orden);
    data.estado = data.estado === "true";
    data.es_publico = false;
    data.icono = "";
    data.fecha_creacion = new Date().toISOString();
    data.fecha_modificacion = new Date().toISOString();

    fetch("/menu", {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => res.json())
      .then(() => {
        editModal.hide();
        fetchMenus();
      });
}
